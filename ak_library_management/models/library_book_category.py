# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryBookCategory(models.Model):
    """ This is a normal model, it is store
        book categories into database """
    _name = 'library.book.category'
    _description = 'Book Category'

    name = fields.Char(string="Category Name", required=True)
    tag_ids = fields.Many2many('library.book.tags', string="Tags")