# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProjectProject(models.Model):
    """ This model is inherited to add a new field named job_name"""
    _inherit = 'project.project'

    job_name = fields.Char(string='Job Name')
