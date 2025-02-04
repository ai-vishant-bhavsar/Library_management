# -*- coding: utf-8 -*-
""" In this module I have """
from odoo import models, fields

class LibraryBook(models.Model):
    """This is a normal model and this model is
       store book data in the database"""
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    publication_date = fields.Date(string="Publication Date")
    category_id = fields.Many2one(comodel_name='library.book.category', string="Category") # this filed is linked with library.book.category by Many2One
    state = fields.Selection(selection=[('available', 'Available'), ('borrowed', 'Borrowed')], string="Availability")
    description = fields.Text(string="Book Summary")
