from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_ids = fields.One2many(
        comodel_name='res.partner.property',
        compute='_get_properties', inverse='set_properties',
        string='Properties'
    )

    @api.multi
    def set_properties(self):
        return

    @api.multi
    def _get_properties(self):
        for record in self:
            property_obj = self.env['res.partner.property']
            values = []
            companies = self.env['res.company'].search([])
            for company in companies:
                val = property_obj.create({
                    'partner_id': record.id,
                    'company_id': company.id
                })
                values.append(val.id)
            record.property_ids = values


class ResPartnerProperty(models.TransientModel):
    _name = 'res.partner.property'
    _inherit = 'multicompany.property.abstract'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )

    @api.one
    def get_properties(self):
        self.get_property_fields(self.partner_id,
                                 self.env['ir.property'].with_context(force_company=self.company_id.id))

    @api.one
    def get_property_fields(self, object, properties):
        return

    @api.model
    def set_properties(self, object, properties=False):
        return
