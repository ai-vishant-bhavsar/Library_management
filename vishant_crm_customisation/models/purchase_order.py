# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrder(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'purchase.order'

    job_name = fields.Char(string='Job Name')
