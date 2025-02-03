# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char('Member Name', required=True)
    email = fields.Char('Email ID')
    phone = fields.Char('Contact Number')
    membership_date = fields.Date('Membership Start Date')
