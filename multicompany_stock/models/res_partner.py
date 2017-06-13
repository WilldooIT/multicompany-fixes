from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_stock_customer = fields.Many2one(readonly=True)
    property_stock_supplier = fields.Many2one(readonly=True)


class ResPartnerProperty(models.TransientModel):
    _inherit = 'res.partner.property'

    property_stock_customer = fields.Many2one(
        'stock.location', string="Customer Location",
        compute='get_properties', inverse='set_property_stock_customer',
        help="This stock location will be used, instead of the default one, as the destination location for goods you send to this partner")
    property_stock_supplier = fields.Many2one(
        'stock.location', string="Vendor Location",
        compute='get_properties', inverse='set_property_stock_supplier',
        help="This stock location will be used, instead of the default one, as the source location for goods you receive from the current partner")

    @api.one
    def get_property_fields(self, object, properties):
        super(ResPartnerProperty, self).get_property_fields(object, properties)
        self.property_stock_customer = self.get_property_value('property_stock_customer', object, properties)
        self.property_stock_supplier = self.get_property_value('property_stock_supplier', object, properties)

    @api.one
    def set_property_stock_customer(self):
        self.set_property_value(self.partner_id, 'property_stock_customer', self.property_stock_customer)

    @api.one
    def set_property_stock_supplier(self):
        self.set_property_value(self.partner_id, 'property_stock_supplier', self.property_stock_supplier)
