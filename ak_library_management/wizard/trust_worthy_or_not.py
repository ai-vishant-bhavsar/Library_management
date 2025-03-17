from odoo import models


class TrustWorthyOrNot(models.Model):
    _inherit = 'borrow.transaction'
    _description = 'Customer is trust worthy or not'