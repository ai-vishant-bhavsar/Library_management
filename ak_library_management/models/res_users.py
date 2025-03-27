# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    """ This model is inheriting res.users
    model and add is_manger filed """
    _inherit = 'res.users'
    _description = 'Is user a manager'

    is_manager = fields.Boolean(string='Is Manager')
