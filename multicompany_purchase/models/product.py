from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_account_creditor_price_difference = fields.Many2one(readonly=True)


class ProductProperty(models.TransientModel):
    _inherit = 'product.template.property'

    purchase_ok = fields.Boolean(related='product_template_id.purchase_ok')
    property_account_creditor_price_difference = fields.Many2one(
        'account.account', string="Price Difference Account",
        compute='get_properties', inverse='set_property_account_creditor_price_difference',
        help="This account will be used to value price difference between purchase price and cost price.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ProductProperty, self).get_property_fields(object, properties)
        self.property_account_creditor_price_difference = self.get_property_value(
            'property_account_creditor_price_difference', object, properties)

    @api.one
    def set_(self):
        self.set_property_value(self.product_template_id, 'property_account_creditor_price_difference',
                                self.property_account_creditor_price_difference)
