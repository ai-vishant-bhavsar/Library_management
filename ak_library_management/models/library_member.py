# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryMember(models.Model):
    """ This store library member details into database """
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char('Member Name', required=True)
    email = fields.Char('Email ID')
    phone = fields.Char('Contact Number')
    membership_date = fields.Date('Membership Start Date')
