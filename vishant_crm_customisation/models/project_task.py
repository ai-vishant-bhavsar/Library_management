from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    job_name = fields.Char(string='Job name')
