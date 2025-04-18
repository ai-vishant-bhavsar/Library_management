from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_project_prepare_values(self):
        """ Inherit method for passing value from sale order to project """
        vals = super(self)._timesheet_create_project_prepare_values()
        vals['job_name'] = f"{self.order_id} - {self.order_id.job_name}"
        return vals
