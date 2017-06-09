from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    property_product_pricelist = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        compute='get_property_product_pricelist',
        inverse='set_property_product_pricelist'
    )

    @api.one
    def get_property_product_pricelist(self):
        self.property_product_pricelist = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_product_pricelist', 'res.partner')

    @api.one
    def set_property_product_pricelist(self):
        self.set_default('property_product_pricelist', 'res.partner',
                         self.property_product_pricelist.id,
                         self.env['ir.property'].with_context(force_company=self.id))