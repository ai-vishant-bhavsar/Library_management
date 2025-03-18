from odoo import models, fields


class BorrowTransactionWarningWizard(models.TransientModel):
    """ Warning Wizard for Borrow Transaction """
    _name = "borrow.transaction.warning.wizard"
    _description = "Borrow Transaction Warning"

    message = fields.Text(string="Warning Message", readonly=True)
    borrow_wizard_id = fields.Many2one(comodel_name="borrow.transaction.history.wizard", string="Borrow Wizard")

    def action_continue(self):
        """ Continue the process from the Borrow Wizard """
        if self.borrow_wizard_id:
            self.borrow_wizard_id._process_transaction()
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """ Cancel the borrow process """
        return {'type': 'ir.actions.act_window_close'}
