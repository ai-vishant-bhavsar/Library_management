# -*- coding: utf-8 -*-
from reportlab.graphics.transform import inverse

from odoo import models, fields, api


class ProductTemplate(models.Model):
    """ This model is inherited from the product
    template and store the book details for the library """
    _inherit = 'product.template'
    _description = 'Product'

    is_library_book = fields.Boolean(string='Library Book')
    author = fields.Char(string='Author')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Data')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    library_id = fields.Many2one(comodel_name="library", string="Library")
    bulk_upload_book = fields.Boolean(string="Bulk upload book", default=False)
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('reserved', 'Reserved'),
            ('overdue', 'Overdue')
        ],
        string='Status',
        default='available',
        required=True,
        tracking=True
    )

    @api.onchange('state')
    def _onchange_state(self):
        for record in self:
            if record.library_id:
                massage = f'{record.name} book state is changed to {record.state}'
                if record.state == 'borrowed':
                    record.env['bus.bus']._sendone(record.library_id.librarian_id, 'rainbow_man_effect', massage)
                elif record.state == 'available':
                    record.env['bus.bus']._sendone(record.library_id.librarian_id, 'rainbow_man_effect', massage)
                elif record.state == 'overdue':
                    record.env['bus.bus']._sendone(record.library_id.librarian_id, 'rainbow_man_effect', massage)

    def action_mark_as_borrowed(self):
        """Mark the book as Borrowed"""
        for record in self:
            record.state = "borrowed"
            record.available = False

    def action_mark_as_available(self):
        """Mark the book as Available"""
        for record in self:
            record.state = "available"
            record.available = True

    def action_borrow_books(self):
        """ This method is action for the borrow book button """
        view = self.env.ref('ak_library_management.view_borrow_transaction_wizard_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books',
            'res_model': 'borrow.transaction.history.wizard',
            'views': [(view.id, 'form')],
            'target': 'new',
        }

    def _compute_display_name(self):
        """ This method is change the display name of books """
        for record in self:
            record.display_name = f"[{record.author}] {record.name}"

    @api.model_create_multi
    def create(self, vals_list):
        """ This method creates a sequence for the new books """
        for vals in vals_list:
            if not vals.get('default_code'):
                vals['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super().create(vals_list)
