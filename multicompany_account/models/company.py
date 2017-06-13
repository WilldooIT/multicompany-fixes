from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    property_account_income_categ_id = fields.Many2one(
        comodel_name='account.account',
        string="Income Account", oldname="property_account_income_categ",
        domain=[('deprecated', '=', False)],
        compute='get_property_account_income_categ_id',
        inverse='set_property_account_income_categ_id',
        help="This account will be used for invoices to value sales.")
    property_account_expense_categ_id = fields.Many2one(
        comodel_name='account.account',
        string="Expense Account",
        oldname="property_account_expense_categ",
        domain=[('deprecated', '=', False)],
        compute='get_property_account_expense_categ_id',
        inverse='set_property_account_expense_categ_id',
        help="This account will be used for invoices to value expenses.")
    property_account_payable_id = fields.Many2one(
        comodel_name='account.account',
        string="Account Payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
        compute='get_property_account_payable_id',
        inverse='set_property_account_payable_id',
        help="This account will be used instead of the default one as the payable account for the current partner"
    )
    property_account_receivable_id = fields.Many2one(
        comodel_name='account.account',
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
        compute='get_property_account_receivable_id',
        inverse='set_property_account_receivable_id',
        help="This account will be used instead of the default one as the receivable account for the current partner"
    )

    @api.one
    def get_property_account_income_categ_id(self):
        self.property_account_income_categ_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_account_income_categ_id', 'product.category')

    @api.one
    def set_property_account_income_categ_id(self):
        self.set_default('property_account_income_categ_id', 'product.category',
                         self.property_account_income_categ_id.id)

    @api.one
    def get_property_account_expense_categ_id(self):
        self.property_account_expense_categ_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_account_expense_categ_id', 'product.category')

    @api.one
    def set_property_account_expense_categ_id(self):
        self.set_default('property_account_expense_categ_id', 'product.category',
                         self.property_account_expense_categ_id.id)

    @api.one
    def get_property_account_payable_id(self):
        self.property_account_payable_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_account_payable_id', 'res.partner')

    @api.one
    def set_property_account_payable_id(self):
        self.set_default('property_account_payable_id', 'res.partner', self.property_account_payable_id.id)

    @api.one
    def get_property_account_receivable_id(self):
        self.property_account_receivable_id = self.env['ir.property'].with_context(force_company=self.id).get(
            'property_account_receivable_id', 'res.partner')

    @api.one
    def set_property_account_receivable_id(self):
        self.set_default('property_account_receivable_id', 'res.partner', self.property_account_receivable_id.id)

