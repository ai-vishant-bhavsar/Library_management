from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    isbn = fields.Char(string="ISBN")
    publication_date = fields.Date(string="Publication Date")
    category_id = fields.Many2one('library.book.category', string="Category")
    tags_ids = fields.Many2many('library.book.tags', string="Tags", related="category_id.tag_ids", readonly=True)
    state = fields.Selection([('available', 'Available'), ('borrowed', 'Borrowed')], string="Availability", default='available')
    description = fields.Text(string="Book Summary")