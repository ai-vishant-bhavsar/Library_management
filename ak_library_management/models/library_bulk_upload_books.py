# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBulkUploadBooks(models.TransientModel):
    """ This transient model is to create one oe more with the
    same Author and the same price and same category at a time """

    _name = "library.bulk.upload.books"
    _description = "Bulk Upload Books"

    book_names = fields.Text(string="Book Names")
    author_id = fields.Many2one(comodel_name="res.partner", string="Author")
    bulk_books_count = fields.Integer(
        string="Product Count",
        compute="_compute_bulk_books_count"
    )
    categories = fields.Many2one(
        comodel_name='library.book.category',
        string="Category"
    )
    price = fields.Float(string='Price', default=100.00)

    def create_products(self):
        """ This function is to add the book into the product.template model """
        if ",," in self.book_names:
            raise ValidationError("Invalid Book Names")
        for book_name in self.book_names.split(','):
            book_name = book_name.strip()

            if not self.env['product.template'].search([('name', '=', book_name), ('is_library_book', '=', True)]):
                product = self.env['product.template'].create([{
                    'name': book_name,
                    'author': self.author_id.name,
                    'is_library_book': True,
                    'bulk_upload_book': True,
                    'list_price': self.price
                }])
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': 'Approval Needed',
                'message': f"books created successfully: {self.book_names} ",
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window_close',
                },
            },
        }

    def revert_changes(self):
        """ This function is to unlink the book which are created in this
        model but not all book it unlink only the running sessions books """
        for book_name in self.book_names.split(','):
            book_name = book_name.strip()
            self.env['product.template'].search([('name', '=', book_name), ('bulk_upload_book', '=', True)]).unlink()

    @api.depends("book_names")
    def _compute_bulk_books_count(self):
        """ This function is to count the created book in running session """
        for record in self:
            record.bulk_books_count = 0
            if record.book_names:
                book_names_list = [book_name.strip() for book_name in record.book_names.split(",")]
                record.bulk_books_count = (record.env['product.template'].
                search_count(
                    [("name", "in", book_names_list), ('is_library_book', '=', True)]))

    def bulk_books(self):
        """ This function is redirect the list view of created books in the current session """
        book_names_list = [book_name.strip() for book_name in self.book_names.split(",")]
        return {
            "name": "Bulk Upload books",
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "list,form",
            "domain": [('bulk_upload_book', '=', True), ('name', 'in', book_names_list)],
            "context": {'create': False},
        }
