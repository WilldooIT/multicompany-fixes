from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_payment_mode_id = fields.Many2one(readonly=True)
    customer_payment_mode_id = fields.Many2one(readonly=True)


class ResPartnerProperties(models.TransientModel):
    _inherit = 'res.partner.property'

    supplier_payment_mode_id = fields.Many2one(
        'account.payment.mode', string='Supplier Payment Mode',
        domain=[('payment_type', '=', 'outbound')],
        compute='get_properties', inverse='set_supplier_payment_mode_id',
        help="Select the default payment mode for this supplier.")
    customer_payment_mode_id = fields.Many2one(
        'account.payment.mode', string='Customer Payment Mode',
        compute='get_properties', inverse='set_customer_payment_mode_id',
        domain=[('payment_type', '=', 'inbound')],
        help="Select the default payment mode for this customer.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ResPartnerProperties, self).get_property_fields(object, properties)
        self.supplier_payment_mode_id = self.get_property_value('supplier_payment_mode_id', object, properties)
        self.customer_payment_mode_id = self.get_property_value('customer_payment_mode_id', object, properties)

    @api.one
    def set_supplier_payment_mode_id(self):
        self.set_property_value(self.partner_id, 'supplier_payment_mode_id', self.supplier_payment_mode_id)

    @api.one
    def set_customer_payment_mode_id(self):
        self.set_property_value(self.partner_id, 'customer_payment_mode_id', self.customer_payment_mode_id)
