# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBulkUploadBooks(models.TransientModel):
    """
    A transient model to allow bulk creation of books as products (product.template).
    Users can enter multiple book names and associate them with an author.
    """

    _name = "library.bulk.upload.books"
    _description = "Bulk Upload Books"

    book_names = fields.Text(string="Book Names")
    author_id = fields.Many2one(comodel_name="res.partner", string="Author")
    bulk_books_count = fields.Integer(string="Product Count",
                                      compute="_compute_bulk_books_count")
    categories = fields.Many2one(comodel_name='library.book.category', string="Category", default="Science-friction")

    def create_products(self):
        """
        This function create multiple books in product.template model.
        which is comma separated books names given input by user.
        """
        # this is condition for user can not give empty book names
        if ",," in self.book_names:
            # Raising Validation Error if book names are not valid
            raise ValidationError("Invalid Book Names")
        for book_name in self.book_names.split(','):
            # removing spaces in to the book name
            book_name = book_name.strip()
            if not bool(self.env['product.template'].search([('name', '=', book_name)])):
                product = self.env['product.template'].create([{
                    'name': book_name,
                    'author': self.author_id.name,
                    'is_library_book': True,
                    'bulk_upload_book': True
                }])

    def revert_changes(self):
        """
        This function revert changes
        If clicked, it will delete all products created
        from the current Bulk Upload Books Record session.
        """
        for book_name in self.book_names.split(','):
            book_name = book_name.strip()
            self.env['product.template'].search([('name', '=', book_name)]).unlink()

    @api.depends("book_names")
    def _compute_bulk_books_count(self):
        """
        This function compute based on the book_names field.
        count the all books or products in the current bulk
        """
        if self.book_names:
            book_names_list = [book_name.strip() for book_name in self.book_names.split(",")]
            self.bulk_books_count = (self.env['product.template'].
                                     search_count([("name", "in", book_names_list)]))
        else:
            self.bulk_books_count = 0  # if book_names has no value so set count to zero

    def bulk_books(self):
        """
        This function redirect to the product list view.
        """
        book_names_list = [book_name.strip() for book_name in self.book_names.split(",")]
        return {
            "name": "Bulk Upload books",
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "list",
            "domain": [('bulk_upload_book','=',True), ('name', 'in', book_names_list)],
            "context": {"create": False},
        }
