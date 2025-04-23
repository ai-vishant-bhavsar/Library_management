# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProjectProject(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'project.project'

    job_name = fields.Char(string='Job Name', compute='_compute_job_from_sale_order', store='True')

    
    @api.depends('sale_order_id.job_name')
    def _compute_job_from_sale_order(self):
        """ This method is to compute the job name from the sale_order.job_name """
        for rec in self:
            rec.job_name = rec.sale_order_id.job_name
