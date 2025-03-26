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
                                     ('state', '=', 'available')])
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
        """ This is checked the customer is member
        or not and then set the deposit amount """
        for customer in self:
            if customer.customer_id.is_member:
                customer.deposit_amount = 0.0
                customer.is_member = True
            else:
                customer.deposit_amount = 50.0
                customer.is_member = False

    def action_confirm(self):
        """ This a confirmation button for the wizard to confirm the action on the wizard and
        save the data of the wiard into the database through the borrow transaction model """
        warnings = self._run_validations()
        if warnings:
            return self._open_warning_wizard(warnings)
        else:
            return self._process_transaction()

    def _run_validations(self):
        """ Run all validations and return warning messages if any """
        warnings = []

        # *Check 1: Customer Trustworthiness*
        if self.customer_id.not_trust_worthy:
            warnings.append("Customer is not trustworthy. Are you sure you want to continue?")

        # *Check 2: Product Availability*
        out_of_stock_books = self.books.filtered(lambda book: book.qty_available <= 0)
        if out_of_stock_books:
            book_list = ", ".join(out_of_stock_books.mapped('name'))
            warnings.append(f"The following books are out of stock: {book_list}. Are you sure you want to continue?")

        # *Check 3: Maximum Books Borrowed*
        existing_transactions = self.env["borrow.transaction.history"].search(
            [("customer_id", "=", self.customer_id.id)])
        total_books_borrowed = len(existing_transactions) + len(existing_transactions.books)

        if total_books_borrowed > 5:
            if existing_transactions:
                warnings.append(
                    f"Customer already has {len(existing_transactions)} open borrow transactions with {len(existing_transactions.books)} books. Are you sure you want to borrow more books?")
            else:
                warnings.append("Are you sure you want to allow borrowing more than 5 books for this customer?")

        return warnings

    def _open_warning_wizard(self, warnings):
        """ Open the warning wizard with messages """
        return {
            "name": "Warning",
            "type": "ir.actions.act_window",
            "res_model": "borrow.transaction.warning.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_message": "\n".join(warnings),
                "default_borrow_wizard_id": self.id
            },
        }

    def _process_transaction(self):
        """ Proceed with the borrow transaction """
        self.env["borrow.transaction.history"].create([{
            "customer_id": self.customer_id.id,
            "books": [(6, 0, self.books.ids)],
            "borrow_start_date": self.borrow_start_date,
            "borrow_end_date": self.borrow_end_date,
            "deposit_amount": self.deposit_amount,
        }])

        # *Decrease stock for borrowed books*
        for book in self.books:
            book.qty_available -= 1
            book.state = 'borrowed'

        return {'type': 'ir.actions.act_window_close'}
