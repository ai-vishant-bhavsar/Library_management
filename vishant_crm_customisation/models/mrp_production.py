# -*- coding: utf-8 -*-
from odoo import models, fields


class MrpProduction(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'mrp.production'

    job_name = fields.Char(string='Job Name')

    def _compute_display_name(self):
        for record in self:
            if record.job_name:
                record.display_name = f"{record.name}{record.job_name}"
            else:
                record.display_name = f"{record.name}"

    def name_get(self):
        res = []
        is_calendar = self.env.context.get('calendar_view', False)
        for record in self:
            name = record.name
            if is_calendar and record.job_name:
                # Use HTML line break for calendar (if HTML allowed)
                name = f"{record.name}<br/>{record.job_name}"
            res.append((record.id, name))
        return res