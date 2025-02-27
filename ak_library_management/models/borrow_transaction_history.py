from datetime import datetime
from odoo import models, fields


class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'

    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer ID')
    books = fields.Many2many(comodel_name='product.template',relation='product_template_id', string="Books", domain="[('is_library_book','=',True)]")
    borrow_start_date = fields.Date(string='Start date', default=datetime.now())
    borrow_end_date = fields.Date(string='End date', )
    deposit_amount = fields.Float(string='Deposit amount')
