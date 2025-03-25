from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _description = "Borrow Transaction History"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    books = fields.Many2many(comodel_name="product.template", string="Borrowed Books",
                             domain=[('sale_ok', '=', True), ('is_library_book', '=', True)])
    borrow_start_date = fields.Date(string="Borrow Start Date", default=datetime.now(), required=True)
    borrow_end_date = fields.Date(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean(string='Customer is member')

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_dates(self):
        """ This method is to check the dates are correctly selected or not """
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("End date cannot be earlier than start date.")

    @api.onchange("customer_id")
    def _onchange_customer(self):
        """ This is checked the customer is member
        or not and then set the deposit amount """
        for customer in self:
            if customer.customer_id.is_member:
                customer.deposit_amount = 0.0
                customer.is_member = True
            else:
                customer.deposit_amount = 50.0
                customer.is_member = False

    def create(self, vals):
        record = super(BorrowTransactionHistory, self).create(vals)
        for book in record.books:
            customer_id = vals.get('customer_id')
            if customer_id:
                # Check if the customer has overdue books
                overdue_books = self.search([
                    ('customer_id', '=', customer_id),
                    ('return_date', '<', fields.Date.today()),
                    (book.state, '=', 'borrowed')
                ])
                if overdue_books:
                    raise exceptions.ValidationError(
                        "You cannot borrow new books until you return your overdue books."
                    )

            if book.state == 'borrowed':
                raise ValidationError('You can not borrow already borrowed books.')
            else:
                book.state = 'borrowed'
                book.message_post(
                    body=f"Book Borrowed: Borrower {record.customer_id.name} on {record.borrow_start_date.strftime('%Y-%m-%d')}.")
        return record

    def unlink(self):
        """ This method is override of unlink, and it will return
        the book and update the status of book borrowed to available"""
        for record in self:
            for book in record.books:
                book.state = 'available'
                book.message_post(
                    body=f"Book Returned: Borrower {record.customer_id.name} on {datetime.today().strftime('%Y-%m-%d')}.")
        return super(BorrowTransactionHistory, self).unlink()

    def send_return_reminder(self):
        """Identify transactions with return dates in the next 2 days and send reminders"""
        today = fields.Date.today()
        upcoming_returns = self.search([
            ('return_date', '>=', today),
            ('return_date', '<=', today + timedelta(days=2)),
            ('state', '=', 'borrowed')
        ])

        mail_template = self.env.ref('your_module.library_return_reminder_email_template')

        for record in upcoming_returns:
            if mail_template:
                mail_template.send_mail(record.id, force_send=True)

    def action_mark_returned(self):
        """Mark books as returned and notify the customer"""
        for record in self:
            record.state = 'returned'  # Update status

            # Send notification
            mail_template = self.env.ref('your_module.library_return_confirmation_email_template')
            if mail_template:
                mail_template.send_mail(record.id, force_send=True)
