# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'sale.order'

    job_name = fields.Char(string='Job Name')

    @api.depends('name')
    def action_confirm(self):
        for order in self:
            if order.opportunity_id:
                order.job_name = order.opportunity_id.name
            if not order.job_name:
                continue
        return super(SaleOrder, self).action_confirm()

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['job_name'] = f"{self.name} - {self.job_name}"
        return invoice_vals
