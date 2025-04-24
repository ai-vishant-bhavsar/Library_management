from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WarningWizard(models.TransientModel):
    """ This model is for pop wizard in the product template for borrow multipal books """
    _name = "warning.wizard"
    _description = "Borrow Books Wizard"

    message = fields.Text(string='warning:')

    def action_cancel(self):
        """ This is action is performed when the wizard cancel button hit """
        rec = self.env["borrow.transaction.history"].search([], order='id desc', limit=1)
        rec.unlink()

    def action_continue(self):
        """ This method is for continue button on wizard """
        rec = self.env["borrow.transaction.history"].search([], order='id desc', limit=1)
        return rec.action_custom_confirm()
