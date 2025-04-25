# -*- coding: utf-8 -*-
from datetime import date

from odoo.exceptions import ValidationError
from reportlab.graphics.transform import inverse
from xlsxwriter.contenttypes import defaults

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
    vendor_on_variants = fields.Boolean(string='Vendor on Variants', default=False)
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned')
        ],
        string='Status',
        default='available',
        tracking=True
    )
    seller_ids_custom = fields.One2many('product.supplierinfo', 'product_id', 'Vendors',
                                        depends_context=('company',))
    variant_seller_ids_custom = fields.One2many('product.supplierinfo', 'product_id')

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
        view = self.env.ref('ak_library_management.view_borrow_transaction_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrow Books',
            'res_model': 'borrow.transaction.history',
            'views': [(view.id, 'form')],
            'target': 'new',
        }

    def _compute_display_name(self):
        """ This method is change the display name of books """
        for record in self:
            record.display_name = f"[{record.author}] {record.name}"

    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """ This method is override for search name by author name"""
        args = list(args or [])
        if name:
            args += [('author', operator, name)]
        return super().name_search(args=args, limit=limit)

    def mark_as_returned(self):
        """ This method is to change the status of return books """
        self.write({'status': 'returned'})

    @api.constrains('state')
    def _check_return_book(self):
        """ This method check the returned books and send the notification to the librarian """
        date_deadline = date.today()
        if self.state == 'returned':
            if date.today() < date_deadline:
                raise ValidationError(f"return date is {date_deadline} "
                                      f"so you can't return book.")
            self.message_post(body=f"{self.env.user.name} is returned the book.")
        if self.state == 'borrowed':
            self.message_post(body=f"{self.env.user.name} is borrowed the book and "
                                   f"the borrow date is {date.today()}")
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': 'warning',
            'message': f"{self.name} book status is changed to {self.state}",
        })

    @api.model_create_multi
    def create(self, vals_list):
        """ This method creates a sequence for the new books """
        for vals in vals_list:
            if not vals.get('default_code'):
                vals['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super().create(vals_list)
