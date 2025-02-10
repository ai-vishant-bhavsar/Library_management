# -*- coding: utf-8 -*-
from odoo import models, fields,api

class Library(models.Model):
    """ This store library details into the database """
    _name = 'library.library'
    _description = 'Library'

    name = fields.Char(string="Library Name", required=True)
    location = fields.Char(string="Location")
    capacity = fields.Integer(string="Capacity")
    notes = fields.Text(string="Notes")
    book_id = fields.Many2many(comodel_name='product.template', string="Books")
    borrowed_book_count = fields.Integer(
        string="Borrowed Books", compute="_compute_borrowed_book_count"
    )

    @api.depends("book_id.state")
    def _compute_borrowed_book_count(self):
        for record in self:
            record.borrowed_book_count = len(record.book_id.filtered(
                lambda b: b.state == "borrowed"))

    def action_view_borrowed_books(self):
        """Open a list view showing all borrowed books from this library."""
        return {
            "name": "Borrowed Books",
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "list",
            "domain": [('id', 'in', self.book_id.ids), ("state", "=", "borrowed")],
            "context": {"create": False},
        }
