# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookTags(models.Model):
    """ This is store book tags into the database """
    _name = 'library.book.tags'
    _description = 'Book Tags'

    name = fields.Char(string="Tag Name", required=True)
