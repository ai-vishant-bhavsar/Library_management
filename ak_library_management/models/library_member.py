# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryMember(models.Model):
    """ This store library member details into database """
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
