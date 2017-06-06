from odoo import models, api, fields


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'multicompany.abstract']

    @api.one
    def get_properties(self):
        super(ProductTemplate, self).get_properties()
        ir_property_obj = self.env['ir.property']
        self.property_stock_procurement = self.get_property(
            self.property,
            'property_stock_procurement',
            ir_property_obj.get('property_stock_procurement', 'product.template'))
        self.property_stock_production = self.get_property(
            self.property,
            'property_stock_production',
            ir_property_obj.get('property_stock_production', 'product.template'))
        self.property_stock_inventory = self.get_property(
            self.property,
            'property_stock_inventory',
            ir_property_obj.get('property_stock_inventory', 'product.template'))

    property_stock_procurement = fields.Many2one(
        'stock.location',
        company_dependent=False,
        compute='get_properties',
        default=get_properties
    )
    property_stock_production = fields.Many2one(
        'stock.location',
        company_dependent=False,
        compute='get_properties',
        default=get_properties
    )
    property_stock_inventory = fields.Many2one(
        'stock.location',
        company_dependent=False,
        compute='get_properties',
        default=get_properties
    )


class ProductProperty(models.Model):
    _inherit = 'product.template.property'

    property_stock_procurement = fields.Many2one(
        'stock.location', "Procurement Location",
        company_dependent=False, domain=[('usage', 'like', 'procurement')],
        help="This stock location will be used, instead of the default one, as the source location for stock moves generated by procurements.")
    property_stock_production = fields.Many2one(
        'stock.location', "Production Location",
        company_dependent=False, domain=[('usage', 'like', 'production')],
        help="This stock location will be used, instead of the default one, as the source location for stock moves generated by manufacturing orders.")
    property_stock_inventory = fields.Many2one(
        'stock.location', "Inventory Location",
        company_dependent=False, domain=[('usage', 'like', 'inventory')],
        help="This stock location will be used, instead of the default one, as the source location for stock moves generated when you do an inventory.")
