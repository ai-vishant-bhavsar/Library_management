from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = "Customers"


    not_trust_worthy = fields.Boolean(string='Not rust worth')
    is_member = fields.Boolean(string='Is member')
