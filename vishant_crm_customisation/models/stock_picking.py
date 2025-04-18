# -*- coding: utf-8 -*-
from odoo import models, fields


class StockPicking(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'stock.picking'

    job_name = fields.Char(string='Job Name')
