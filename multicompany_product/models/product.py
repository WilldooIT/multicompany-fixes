import odoo.addons.decimal_precision as dp

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(readonly=True)

    property_ids = fields.One2many(
        comodel_name='product.template.property',
        compute='_get_properties', inverse='set_properties',
        string='Properties'
    )

    @api.multi
    def set_properties(self):
        return

    @api.multi
    def _get_properties(self):
        for record in self:
            property_obj = self.env['product.template.property']
            values = []
            companies = self.env['res.company'].search([])
            for company in companies:
                val = property_obj.create({
                    'product_template_id': record.id,
                    'company_id': company.id
                })
                values.append(val.id)
            record.property_ids = values


class ProductProperty(models.TransientModel):
    _name = 'product.template.property'
    _inherit = 'multicompany.property.abstract'

    _description = "Properties of Product categories"

    product_template_id = fields.Many2one(
        comodel_name='product.template',
        string="Product"
    )

    standard_price = fields.Float(
        'Cost',
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="Cost of the product template used for standard stock valuation in accounting and used as a base price on purchase orders. "
             "Expressed in the default unit of measure of the product.",
        compute='get_properties', inverse='set_standard_price')

    @api.one
    def get_properties(self):
        self.get_property_fields(self.product_template_id,
                                 self.env['ir.property'].with_context(force_company=self.company_id.id))

    @api.one
    def get_property_fields(self, object, properties):
        self.standard_price = self.get_property_value('standard_price', object, properties)

    @api.one
    def set_standard_price(self):
        self.set_property_value(self.product_template_id, 'standard_price', self.standard_price)
