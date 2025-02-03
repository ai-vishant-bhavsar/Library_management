# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    _sql_constraints = [
        ('unique_custom_name', 'unique(custom_name)', 'Custom category name must be unique!')
    ]

    CATEGORY_SELECTION = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('fantasy', 'Fantasy'),
        ('custom', 'Custom'),  # Option for custom category
    ]

    name = fields.Selection(selection=CATEGORY_SELECTION, string="Category", required=True)
    custom_name = fields.Char(string="Custom Category", unique=True)  # Unique constraint
    tag_ids = fields.Many2many('library.book.tags', string="Tags")

    @api.constrains('custom_name')
    def _check_custom_name_unique(self):
        """ Ensure unique custom category names """
        for record in self:
            if record.name == 'custom' and record.custom_name:
                existing = self.search([('custom_name', '=', record.custom_name), ('id', '!=', record.id)])
                if existing:
                    raise ValidationError("Custom category name must be unique!")

    @api.onchange('name')
    def _onchange_name(self):
        """ Clear custom category when a predefined one is selected """
        if self.name != 'custom':
            self.custom_name = False