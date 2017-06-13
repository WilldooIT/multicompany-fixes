from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_creditor_price_difference_categ = fields.Many2one(readonly=True)


class ProductCategoryProperty(models.TransientModel):
    _inherit = 'product.category.property'

    property_account_creditor_price_difference_categ = fields.Many2one(
        'account.account', string="Price Difference Account",
        compute='get_properties', inverse='set_property_account_creditor_price_difference_categ',
        help="This account will be used to value price difference between purchase price and accounting cost.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ProductCategoryProperty, self).get_property_fields(object, properties)
        self.property_account_creditor_price_difference_categ = self.get_property_value(
            'property_account_creditor_price_difference_categ', object, properties)

    @api.one
    def set_property_account_creditor_price_difference_categ(self):
        self.set_property_value(self.categ_id, 'property_account_creditor_price_difference_categ',
                                self.property_account_creditor_price_difference_categ)
