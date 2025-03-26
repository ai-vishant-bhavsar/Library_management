# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Configration Settings'

    borrow_limit = fields.Integer(string='Borrow Limit')
