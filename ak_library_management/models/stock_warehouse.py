# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _description = 'Stock warehouse'

    library_assistant = fields.Many2one(comodel_name='hr.employee', string='Library assistant')
    library_worker = fields.Many2many(comodel_name='hr.employee', string='Library worker')

    @api.constrains('library_assistant', 'library_worker')
    def _check_library_assistant(self):
        for record in self:
            for val in record.library_worker:
                if record.library_assistant == val:
                    raise ValidationError(
                        f"You can not select [{record.library_assistant.name}] as both an Assistant and a Worker")
