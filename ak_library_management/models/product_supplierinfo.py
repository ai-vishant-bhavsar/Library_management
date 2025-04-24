from odoo import models, api, fields
from odoo.exceptions import ValidationError


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'
    from odoo import models, fields, api

    class ParentModel(models.Model):
        _name = 'parent.model'

        name = fields.Char(string="Parent Name")
        child_ids = fields.One2many('child.model', 'parent_id', string="Child Records", compute='_compute_child_ids',
                                    inverse='_inverse_child_ids')

        @api.depends('name')
        def _compute_child_ids(self):
            for record in self:
                # Replace with your conditional logic
                if record.name == 'Condition A':
                    record.child_ids = self.env['child.model'].search([('name', '=', 'Child A')])
                elif record.name == 'Condition B':
                    record.child_ids = self.env['child.model'].search([('name', '=', 'Child B')])
                else:
                    record.child_ids = self.env['child.model']

        def _inverse_child_ids(self):
            # Replace with your logic to update child records
            pass

    class ChildModel(models.Model):
        _name = 'child.model'

        name = fields.Char(string="Child Name")
        parent_id = fields.Many2one('parent.model', string="Parent")

    def create(self, vals_list):
        """ Prevents auto-creating vendors on all variants when 'Vendor on Variants' is True """
        for vals in vals_list:
            product_id = vals.get('product_id.id')
            tmpl_id = vals.get('product_tmpl_id')
            print(self.product_id.id)

            if tmpl_id:
                template = self.env['product.template'].browse(tmpl_id)
                if template.vendor_on_variants and not product_id:
                    raise ValidationError(
                        "You cannot assign a vendor to the product template when 'Vendor on Variants' is enabled. Assign it to individual variants instead.")

        return super().create(vals_list)
