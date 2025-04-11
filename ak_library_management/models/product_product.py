from odoo import models,fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    seller_ids= fields.One2many('product.supplierinfo', 'product_id', 'Vendors',
                                 depends_context=('company',))
    variant_seller_ids = fields.One2many('product.supplierinfo', 'product_id')