from odoo.api import depends

from odoo import models, fields, api, exceptions


class SaleOrder(models.Model):
    """ This model is inherited from sale.order model
    to perform the methods only for books """
    _inherit = 'sale.order'

    approval_needed = fields.Boolean(string='Approval Needed', compute='_compute_approval_needed', store=True)
    approved_by_manager = fields.Boolean(string='Approved by Manager', default=False)

    @api.depends('order_line.product_uom_qty')
    def _compute_approval_needed(self):
        """ This method is to count the low stock books
         and store boolean in approval_needed field"""
        for order in self:
            low_stock_books = order.order_line.filtered(lambda l: l.product_uom_qty < 5)
            order.approval_needed = bool(low_stock_books)

    def action_confirm(self):
        """ This method is override and add a validation for the
        approval_needed and approved_by_manager both fields """
        if self.approval_needed and not self.approved_by_manager:
            low_stock_books = self.order_line.filtered(lambda l: l.product_id.qty_available < 5).mapped('product_id.display_name')
            raise exceptions.UserError(f"Approval needed! The following books have low stock: {', '.join(low_stock_books)}")
        else:
            return super(SaleOrder, self).action_confirm()

    @depends('approved_by_manager')
    def action_approve(self):
        """ This method is for approve button to approve low stoke books order"""
        if not self.env.user.is_manager:
            raise exceptions.AccessError("Only managers can approve orders.")
        else:
            self.approved_by_manager = True
