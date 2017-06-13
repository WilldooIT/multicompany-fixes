from odoo import fields, models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_income_categ_id = fields.Many2one(readonly=True)
    property_account_expense_categ_id = fields.Many2one(readonly=True)


class ProductCategoryProperty(models.TransientModel):
    _inherit = 'product.category.property'

    property_account_income_categ_id = fields.Many2one(
        comodel_name='account.account',
        string="Income Account", oldname="property_account_income_categ",
        domain=[('deprecated', '=', False)],
        compute='get_properties', inverse='set_property_account_income_categ_id',
        help="This account will be used for invoices to value sales.")
    property_account_expense_categ_id = fields.Many2one(
        comodel_name='account.account',
        string="Expense Account",
        oldname="property_account_expense_categ",
        domain=[('deprecated', '=', False)],
        compute='get_properties', inverse='set_property_account_expense_categ_id',
        help="This account will be used for invoices to value expenses.")

    @api.one
    def get_property_fields(self, object, properties):
        super(ProductCategoryProperty, self).get_property_fields(object, properties)
        self.property_account_income_categ_id = self.get_property_value('property_account_income_categ_id', object,
                                                                        properties)
        self.property_account_expense_categ_id = self.get_property_value('property_account_expense_categ_id', object,
                                                                         properties)

    @api.one
    def set_property_account_income_categ_id(self):
        self.set_property_value(self.categ_id, 'property_account_income_categ_id',
                                self.property_account_income_categ_id)

    @api.one
    def set_property_account_expense_categ_id(self):
        self.set_property_value(self.categ_id, 'property_account_expense_categ_id',
                                self.property_account_expense_categ_id)
