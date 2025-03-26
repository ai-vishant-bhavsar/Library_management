# -*- coding: utf-8 -*-
from odoo import _, models, fields, api


class LibraryMember(models.Model):
    """ This store library member details into database """
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    membership_no = fields.Char(
        string="Membership ID",
        readonly=True,
        default=lambda self: _('New')
    )

    @api.model_create_multi
    def create(self, vals_list):
        """This method creates a member sequence for library member"""
        for vals in vals_list:
            if not vals.get('membership_no'):
                vals['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
        return super().create(vals_list)

    def copy(self, default=None):
        """ This method copies the data from the current data and changes the sequence """
        default = dict(default or {})
        default['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
        return super().copy(default)
