# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryBookCategory(models.Model):
    """ This is a normal model, it is store
        the categories for the books """
    _name = 'library.book.category'
    _description = 'Book Category'

    name = fields.Char(string="Category Name", required=True)
    description = fields.Text(string="Description")
