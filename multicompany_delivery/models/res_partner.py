from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_delivery_carrier_id = fields.Many2one(readonly=True)


class ResPartnerProperty(models.TransientModel):
    _inherit = 'res.partner.property'

    property_delivery_carrier_id = fields.Many2one(
        'delivery.carrier',
        string="Delivery Method",
        compute='get_properties', inverse='set_property_delivery_carrier_id',
        help="This delivery method will be used when invoicing from picking.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ResPartnerProperty, self).get_property_fields(object, properties)
        self.property_delivery_carrier_id = self.get_property_value('property_delivery_carrier_id', object, properties)

    @api.one
    def set_property_delivery_carrier_id(self):
        self.set_property_value(self.partner_id, 'property_delivery_carrier_id', self.property_delivery_carrier_id)
