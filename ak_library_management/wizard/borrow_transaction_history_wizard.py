from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class BorrowTransactionHistoryWizard(models.TransientModel):
    """ This model is for pop wizard in the product template for borrow multipal books """
    _name = "borrow.transaction.history.wizard"
    _description = "Borrow Books Wizard"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    books = fields.Many2many(comodel_name="product.template", string="Books",
                             domain=[('sale_ok', '=', True), ('is_library_book', '=', True),
                                     ('state', '=', 'borrowed')])
    borrow_start_date = fields.Date(string="From Date", default=datetime.now())
    borrow_end_date = fields.Date(string="End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean(string='Customer is member')

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_dates(self):
        """ This method is to check the dates are correct or not """
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("End date cannot be earlier than start date.")

    @api.onchange("customer_id")
    def _onchange_customer(self):
        for customer in self:
            if customer.customer_id.is_member:
                customer.deposit_amount = 0.0
                customer.is_member = True
            else:
                customer.deposit_amount = 50.0
                customer.is_member = False

    def action_confirm(self):
        """ This a confirm button for the wizard to confirm the action on the wizard and
        save the data of the wiard into the database through the borrow transaction model """

        # Check if customer is trustworthy
        if self.customer_id.not_trust_worthy:
            raise UserError('Customer is not trust worthy. Are you sure you want to continue?')

        # Check maximum borrow limit
        existing_transactions = self.env["borrow.transaction.history"].search_count(
            [("customer_id", "=", self.customer_id.id)])
        total_books = len(self.books) + existing_transactions
        if total_books > 5:
            raise UserError("Customer is exceeding the 5-book limit. Are you sure you want to continue?")

        # Create borrow transaction
        else:
            self.env["borrow.transaction.history"].create([{
                "customer_id": self.customer_id.id,
                "books": [(6, 0, self.books.ids)],
                "borrow_start_date": self.borrow_start_date,
                "borrow_end_date": self.borrow_end_date,
                "deposit_amount": self.deposit_amount,
            }])
