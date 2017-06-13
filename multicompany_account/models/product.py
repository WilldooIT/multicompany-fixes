from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_account_income_id = fields.Many2one(readonly=True)
    property_account_expense_id = fields.Many2one(readonly=True)


class ProductProperty(models.TransientModel):
    _inherit = 'product.template.property'

    property_account_income_id = fields.Many2one(
        comodel_name='account.account',
        string="Income Account",
        domain=[('deprecated', '=', False)],
        compute='get_properties', inverse='set_property_account_income_id',
        help="This account will be used for invoices instead of the default one to value sales for the current product."
    )
    property_account_expense_id = fields.Many2one(
        comodel_name='account.account',
        string="Expense Account",
        domain=[('deprecated', '=', False)],
        compute='get_properties', inverse='set_property_account_expense_id',
        help="This account will be used for invoices instead of the default one to value expenses for the current product.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ProductProperty, self).get_property_fields(object, properties)
        self.property_account_income_id = self.get_property_value('property_account_income_id', object, properties)
        self.property_account_expense_id = self.get_property_value('property_account_expense_id', object, properties)

    @api.one
    def set_property_account_income_id(self):
        self.set_property_value(self.product_template_id, 'property_account_income_id',
                                self.property_account_income_id)

    @api.one
    def set_property_account_expense_id(self):
        self.set_property_value(self.product_template_id, 'property_account_expense_id',
                                self.property_account_expense_id)
