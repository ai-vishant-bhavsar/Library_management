# -*- coding: utf-8 -*-
from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super()._prepare_purchase_order(company_id=company_id, origins=origins, values=values)
        res['job_name'] = values[0].get("job_name")
        return res

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id,
                         name, origin, company_id, values, bom, ):
        vals = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom,
                                                       location_id, name, origin, company_id,
                                                       values, bom, )
        vals["job_name"] = values.get("job_name")
        return vals


