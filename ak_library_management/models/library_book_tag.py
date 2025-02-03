from odoo import models, fields

class LibraryBookTags(models.Model):
    _name = 'library.book.tags'
    _description = 'Book Tags'

    name = fields.Char(string="Tag Name", required=True)