from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.Model):
    _name = "borrow.transaction.history"
    _description = "Borrow Transaction History"

    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    books = fields.Many2many(comodel_name="product.template", string="Borrowed Books",
                             domain=[('sale_ok', '=', True), ('is_library_book', '=', True),
                                     ('state', '=', 'borrowed')])
    borrow_start_date = fields.Date(string="Borrow Start Date", default=datetime.now(), required=True)
    borrow_end_date = fields.Date(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")

    @api.constrains('borrow_end_date', 'borrow_start_date')
    def _check_dates(self):
        for record in self:
            if record.borrow_end_date < record.borrow_start_date:
                raise ValidationError("End date cannot be earlier than start date.")

    @api.onchange("customer_id")
    def _onchange_customer(self):
        if self.customer_id:
            self.deposit_amount = 0.0 if self.customer_id.is_member else 50.0
