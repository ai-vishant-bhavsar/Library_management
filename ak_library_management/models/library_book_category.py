# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryBookCategory(models.Model):
    """ This is a normal model, it is store
        book categories into database """
    _name = 'library.book.category'
    _description = 'Book Category'

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
    custom_name = fields.Char(string="Custom Category")
    tag_ids = fields.Many2many('library.book.tags', string="Tags")