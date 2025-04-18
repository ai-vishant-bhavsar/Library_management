# -*- coding: utf-8 -*-
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    job_name = fields.Char(string="Job Name")

    def _get_new_picking_values(self):
        res = super(StockMove,self)._get_new_picking_values()
        res["job_name"] = self.group_id.sale_id.job_name
        return res

    def _prepare_procurement_values(self):
        values = super()._prepare_procurement_values()
        values['job_name'] = self.group_id.sale_id.job_name
        return values

    def _prepare_purchase_values(self, company_id, origins, values):
        res = super()._prepare_purchase_order(company_id=company_id, origins=origins, values=values)
        res['sale'] = self.group_id.sale_id
        return res
