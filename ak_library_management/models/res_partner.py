from odoo import models, fields


class ResPartner(models.Model):
    """ This is model is inherited from res.partner to add
     the 2 new fields not_trust_worthy and is_member """
    _inherit = 'res.partner'
    _description = "Customers"


    not_trust_worthy = fields.Boolean(string='Not trust worthy')
    is_member = fields.Boolean(string='Is member')
