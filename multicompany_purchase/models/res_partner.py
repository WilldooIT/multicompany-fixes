from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_purchase_currency_id = fields.Many2one(readonly=True)


class ResPartnerProperties(models.TransientModel):
    _inherit = 'res.partner.property'

    property_purchase_currency_id = fields.Many2one(
        'res.currency', string="Supplier Currency",
        compute='get_properties', inverse='set_property_purchase_currency_id',
        help="This currency will be used, instead of the default one, for purchases from the current partner")

    @api.one
    def get_property_fields(self, object, properties):
        super(ResPartnerProperties, self).get_property_fields(object, properties)
        self.property_purchase_currency_id = self.get_property_value('property_purchase_currency_id', object, properties)

    @api.one
    def set_property_purchase_currency_id(self):
        self.set_property_value(self.partner_id, 'property_purchase_currency_id', self.property_purchase_currency_id)
