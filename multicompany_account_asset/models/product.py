from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    asset_category_id = fields.Many2one(readonly=True)
    deferred_revenue_category_id = fields.Many2one(readonly=True)


class ProductProperty(models.TransientModel):
    _inherit = 'product.template.property'

    asset_category_id = fields.Many2one(
        'account.asset.category',
        string='Asset Type',
        compute='get_properties', inverse='set_asset_category_id',
        ondelete="restrict")
    deferred_revenue_category_id = fields.Many2one(
        'account.asset.category',
        string='Deferred Revenue Type',
        compute='get_properties', inverse='set_deferred_revenue_category_id',
        ondelete="restrict")

    @api.one
    def get_property_fields(self, object, properties):
        super(ProductProperty, self).get_property_fields(object, properties)
        self.asset_category_id = self.get_property_value('asset_category_id', object, properties)
        self.deferred_revenue_category_id = self.get_property_value('deferred_revenue_category_id', object, properties)

    @api.one
    def set_asset_category_id(self):
        self.set_property_value(self.product_template_id, 'asset_category_id',
                                self.asset_category_id)

    @api.one
    def set_deferred_revenue_category_id(self):
        self.set_property_value(self.product_template_id, 'deferred_revenue_category_id',
                                self.deferred_revenue_category_id)