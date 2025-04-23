# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'sale.order'

    job_name = fields.Char(string='Job Name')

    def _prepare_invoice(self):
        """ This method is to prepare the invoice values and pass them to inovice """
        invoice_vals = super()._prepare_invoice()
        invoice_vals['job_name'] = f"{self.name} - {self.job_name}"
        return invoice_vals
