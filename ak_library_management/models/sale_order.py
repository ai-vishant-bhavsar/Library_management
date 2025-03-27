# -*- coding: utf-8 -*-
from odoo.api import depends, onchange, Environment
from odoo import models, fields, api, exceptions


class SaleOrder(models.Model):
    """ This model is inherited from sale.order
    model to perform the methods only for books """
    _inherit = 'sale.order'

    approval_needed = fields.Boolean(string='Approval Needed', default=False, compute='_compute_approval_needed',
                                     store=True)
    approved_by_manager = fields.Boolean(string='Approved by Manager', default=False)
    hide_button = fields.Boolean(string='Hide button', default=False)

    @api.depends('order_line.product_uom_qty')
    def _compute_approval_needed(self):
        """ This method is to count the low stock books
         and store boolean in approval_needed field """
        for order in self:
            low_stock_books = order.order_line.filtered(lambda l: l.product_uom_qty < 5)
            order.approval_needed = bool(low_stock_books)

    def action_confirm(self):
        """ Override method to check approval before confirming """
        for order in self:
            if order.approval_needed and not order.approved_by_manager:
                order.write({'hide_button': True})
                self.env.cr.commit()
                low_stock_books = order.order_line.filtered(
                    lambda l: l.product_id.qty_available < 5
                ).mapped('product_id.display_name')
                return {
                    'type': 'ir.actions.client',
                    'tag': 'rainbow_man_effect',
                    'params': {
                        'type': 'warning',
                        'title': 'Approval Needed',
                        'message': f"Approval needed! The following books have low stock: {', '.join(low_stock_books)}",
                        'sticky': False,
                        'next': {
                            'type': 'ir.actions.act_window_close',
                        },
                    },
                }

        return super(SaleOrder, self).action_confirm()

    @depends('approved_by_manager')
    def action_approve(self):
        """ This method is for approve button to approve low stock books order """
        for order in self:
            if not order.env.user.is_manager:
                raise exceptions.AccessError("Only managers can approve orders.")
            else:
                order.approved_by_manager = True
                order.hide_button = False
