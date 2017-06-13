from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    property_stock_journal = fields.Many2one(
        comodel_name='account.journal',
        required=False,
        string="Default stock Journal",
        compute='get_property_stock_journal', inverse='set_property_stock_journal'
    )
    property_stock_account_input_categ_id = fields.Many2one(
        comodel_name='account.account',
        required=False,
        string="Default stock input account for category",
        compute='get_property_stock_account_input_categ_id', inverse='set_property_stock_account_input_categ_id'
    )
    property_stock_account_output_categ_id = fields.Many2one(
        comodel_name='account.account',
        required=False,
        string="Default stock output account for category",
        compute='get_property_stock_account_output_categ_id', inverse='set_property_stock_account_output_categ_id',
    )
    property_stock_account_input = fields.Many2one(
        comodel_name='account.account',
        required=False,
        string="Default stock input account for Template",
        compute='get_property_stock_account_input', inverse='set_property_stock_account_input'
    )
    property_stock_account_output = fields.Many2one(
        comodel_name='account.account',
        required=False,
        string="Default stock output account for Template",
        compute='get_property_stock_account_output', inverse='set_property_stock_account_output',
    )
    property_stock_valuation_account_id = fields.Many2one(
        comodel_name='account.account',
        required=False,
        string="Default stock valuation account",
        compute='get_property_stock_valuation_account_id',
        inverse='set_property_stock_valuation_account_id'
    )

    @api.one
    def get_property_stock_journal(self):
        self.property_stock_journal = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_journal', 'product.category')

    @api.one
    def set_property_stock_journal(self):
        self.set_default('property_stock_journal', 'product.category', self.property_stock_journal.id)

    @api.one
    def get_property_stock_account_input_categ_id(self):
        self.property_stock_account_input_categ_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_account_input_categ_id',
            'product.category')

    @api.one
    def set_property_stock_account_input_categ_id(self):
        self.set_default('property_stock_account_input_categ_id', 'product.category',
                         self.property_stock_account_input_categ_id.id)

    @api.one
    def get_property_stock_account_output_categ_id(self):
        self.property_stock_account_output_categ_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_account_output_categ_id',
            'product.category')

    @api.one
    def set_property_stock_account_output_categ_id(self):
        self.set_default('property_stock_account_output_categ_id', 'product.category',
                         self.property_stock_account_output_categ_id.id)

    @api.one
    def get_property_stock_account_input(self):
        self.property_stock_account_input = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_account_input',
            'product.template')

    @api.one
    def set_property_stock_account_input(self):
        self.set_default('property_stock_account_input', 'product.template',
                         self.property_stock_account_input.id)

    @api.one
    def get_property_stock_account_output(self):
        self.property_stock_account_output = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_account_output',
            'product.template')

    @api.one
    def set_property_stock_account_output(self):
        self.set_default('property_stock_account_output', 'product.template',
                         self.property_stock_account_output.id)

    @api.one
    def get_property_stock_valuation_account_id(self):
        self.property_stock_valuation_account_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_stock_valuation_account_id',
            'product.category')

    @api.one
    def set_property_stock_valuation_account_id(self):
        self.set_default('property_stock_valuation_account_id', 'product.category',
                         self.property_stock_valuation_account_id.id)
