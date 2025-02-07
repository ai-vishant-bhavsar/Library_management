# -*- coding: utf-8 -*-
from odoo import models, fields

class LibraryBook(models.Model):
    """ This is store library books details into the database """
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    publication_date = fields.Date(string="Publication Date")
    category_id = fields.Many2one(comodel_name='library.book.category', string="Category")
    tags_ids = fields.Many2many(comodel_name='library.book.tags', string="Tags", related="category_id.tag_ids")
    state = fields.Selection(selection=[('available', 'Available'), ('borrowed', 'Borrowed')], string="Availability")
    description = fields.Text(string="Book Summary")
    library_id = fields.Many2one(comodel_name='library.library', string="Library")
