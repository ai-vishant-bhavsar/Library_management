# -*- coding: utf-8 -*-
from odoo import models, fields

class Library(models.Model):
    """ This normal model it is store
        library details into the database """
    _name = 'library.library'
    _description = 'Library'

    name = fields.Char(string="Library Name", required=True)
    location = fields.Char(string="Location")
    capacity = fields.Integer(string="Capacity")
    notes = fields.Text(string="Notes")
    book_ids = fields.One2many('library.book', 'library_id', string="Books")