# -*- coding: utf-8 -*-
from odoo import models,fields

class ProductTemplate(models.Model):
    """ This model is inherited from the product
    template and store the book details for library """
    _inherit = 'product.template'
    _description = 'Product'

    is_library_book = fields.Boolean(string='Library Book')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_data = fields.Date(string='Published Data')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    library_id = fields.Many2one(comodel_name="library.library", string="Library")
    state = fields.Selection(
        selection=[
            ("available", "Available"),
            ("borrowed", "Borrowed"),
            ("reserved", "Reserved"),
        ],
        string="Status",
        default="available",
        required=True,
    )

    def action_mark_as_borrowed(self):
        """Mark the book as Borrowed"""
        for record in self:
            record.state = "borrowed"

    def action_mark_as_available(self):
        """Mark the book as Available"""
        for record in self:
            record.state = "available"
