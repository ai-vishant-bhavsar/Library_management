from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Borrow Transaction History"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    books = fields.Many2many(comodel_name="product.template", string="Borrowed Books",
                             domain=[('sale_ok', '=', True), ('is_library_book', '=', True)])
    borrow_start_date = fields.Date(string="Borrow Start Date", default=datetime.now(), required=True)
    borrow_end_date = fields.Date(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean(related='customer_id.is_member')
    is_active = fields.Boolean(compute='_compute_active_transaction', store=True)
    is_out_of_limit = fields.Boolean(compute='_compute_more_than_borrow_limit', default=False, store=True)

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_dates(self):
        """ This method is to check the dates are correctly selected or not """
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("End date cannot be earlier than start date.")

    @api.depends('customer_id')
    def _compute_more_than_borrow_limit(self):
        """ This compute method is checking the current transaction of customer """
        for record in self:
            borrow_transaction_ids = record.search([('customer_id.id', "=", record.customer_id.id)])
            books_name = [book.name for record in borrow_transaction_ids
                          for book in record.books]
            if len(books_name) > int(record.env['ir.config_parameter'].
                                             get_param('ak_library_management.borrow_limit')):
                record.is_higher_than_limit = True

    @api.depends('borrow_end_date')
    def _compute_active_transaction(self):
        """ This method is to check the traction is active or not """
        for record in self:
            record.is_active = record.borrow_end_date >= date.today()

    @api.onchange("customer_id")
    def _onchange_customer(self):
        """ This is checked the customer is member
        or not and then set the deposit amount """
        for customer in self:
            if customer.customer_id.is_member:
                customer.deposit_amount = 0.0
            else:
                customer.deposit_amount = 50.0

    def _schedule_overdue_books(self):
        """ This method is for scheduler action to check the overdue book for send a mail """
        borrow_transaction_ids = self.search([('borrow_end_date', '<', date.today()),
                                              ('books.state', '=', 'borrowed')])

        for record in borrow_transaction_ids:
            template = record.env.ref('ak_library_management.overdue_book_email_template')
            template.send_mail(record.id, force_send=True)

    def create(self, vals):
        record = super(BorrowTransactionHistory, self).create(vals)
        for book in self.books:
            customer_id = vals.get('customer_id')
            if customer_id:
                # Check if the customer has overdue books
                overdue_books = self.search([
                    ('customer_id', '=', customer_id),
                    ('borrow_end_date', '<', fields.Date.today()),
                ])
                if overdue_books:
                    raise ValidationError(
                        "You cannot borrow new books until you return your overdue books."
                    )

            if customer_id.not_trust_worthy:
                message = "Customer is not trustworthy. Are you sure you want to continue?"
                yield self.warning_wizard(message)

            product_list = [rec.name for rec in self.books if int(rec.qty_available) == 0]
            if product_list:
                message = (f"The following books are out of stock: {product_list}."
                           f" Are you sure you want to continue?")
                yield self.warning_wizard(message)

            if len(self.books) > 5:
                borrow_transaction_ids = self.search([('customer_id', "=", self.customer_id.id)],
                                                     order='id desc', offset=1)
                books_name = []
                [books_name.append(book.name) for book in borrow_transaction_ids.books.filtered(
                    lambda x: x.name not in books_name)]
                if books_name:
                    message = (f"Customer already has [{len(borrow_transaction_ids)}] open "
                               f"borrow transactions with {books_name} books. "
                               f"Are you sure you want to borrow more books?")
                    yield self.warning_wizard(message)
                else:
                    message = ("Are you sure you want to allow "
                               "borrowing more than 5 books for this customer?")
                    yield self.warning_wizard(message)

            if book.state == 'borrowed':
                raise ValidationError('You can not borrow already borrowed books.')
            else:
                book.state = 'borrowed'
                book.message_post(
                    body=f"Book Borrowed: Borrower {record.customer_id.name} on {record.borrow_start_date.strftime('%Y-%m-%d')}.")
                record._create_due_date_activity()
        return record

    def warning_wizard(self, message):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'warning.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_message': message,
                'books': [book.id for book in self.books],
            }
        }

    def unlink(self):
        """ This method is override of unlink, and it will return
        the book and update the state of book borrowed to available"""
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
            ('borrow_end_date', '>=', today),
            ('borrow_end_date', '<=', today + timedelta(days=2)),
        ])

        mail_template = self.env.ref('ak_library_management.library_return_reminder_email_template')

        for record in upcoming_returns:
            if mail_template:
                mail_template.send_mail(record.id, force_send=True)

    def _schedule_overdue_return(self):
        borrow_transaction_ids = self.search([('borrow_end_date', '<', date.today()),
                                              ('books.state', '=', 'borrowed')])

        for rec in borrow_transaction_ids:
            template = self.env.ref('ak_library_management.overdue_book_email_template')
            template.send_mail(rec.id, force_send=True)

    def action_mark_returned(self):
        """Mark books as returned and notify the customer"""
        for record in self:
            record.state = 'returned'  # Update state

            # Send notification
            mail_template = self.env.ref('your_module.library_return_confirmation_email_template')
            if mail_template:
                mail_template.send_mail(record.id, force_send=True)

    def action_change_borrowed_book_state(self):
        """ change the book state from borrowed to return using server action """
        for rec in self.search([('books.state', '=', 'borrowed')]):
            for book in rec.books:
                self.env['bus.bus']._sendone(rec.customer_id, 'simple_notification', {
                    'type': 'warning',
                    'message': f"{rec.customer_id.name} your return book has been recorded.",
                })
                book.mark_as_returned()

    def _create_due_date_activity(self):
        """Creates an automated To-Do activity for the current user"""
        activity_type = self.env.ref('mail.mail_activity_data_todo')  # Get To-Do activity type
        current_user = self.env.user  # Get the current logged-in user

        for record in self:
            record.env['mail.activity'].create([{
                'res_model_id': self.env['ir.model']._get_id('borrow.transaction.history'),
                'res_id': record.id,
                'activity_type_id': activity_type.id,
                'summary': f"Return Book Reminder: {record.books.name}",
                'note': f"Borrower: {record.customer_id.name}<br/>"
                        f"Due Date: {record.borrow_end_date.strftime('%Y-%m-%d')}",
                'user_id': current_user.id,
                'date_deadline': record.borrow_end_date,
            }])
