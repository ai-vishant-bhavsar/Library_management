from odoo import models, fields


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """ Method for passing value from sale order to regular invoice. """
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        res.update({"job_name": order.job_name})
        return res
