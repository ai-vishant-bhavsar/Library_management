# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookCategory(models.Model):
    """ This is store book categories into database """
    _name = 'library.book.category'
    _description = 'Book Category'

    name = fields.Char(string="Category")
    tag_ids = fields.Many2many(
        comodel_name='library.book.tags',
        string="Tags")
