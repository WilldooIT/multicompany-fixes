# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        res = []
        names = super(SaleOrder, self).name_get()
        multicompany_group = self.env.ref('base.group_multi_company')
        if multicompany_group not in self.env.user.groups_id:
            return names
        for name in names:
            rec = self.browse(name[0])
            name = '%s [%s]' % (name[1], rec.company_id.name) if \
                rec.company_id else name[1]
            res += [(rec.id, name)]
        return res

    @api.model
    def create(self, vals):
        """ Influence the default values in related comodels, if we reach to
        this point and no value has yet been provided """
        if 'company_id' in vals:
            updated_self = self.with_context(force_company=vals['company_id'])
        else:
            updated_self = self
        return super(SaleOrder, updated_self).create(vals)

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id and self.team_id.company_id:
            self.company_id = self.team_id.company_id

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.env.context = self.with_context(
            force_company=self.company_id.id).env.context
        return super(SaleOrder, self).onchange_partner_id()

    @api.multi
    @api.onchange('company_id')
    def onchange_company_id(self):
        res = {}
        if self.partner_id and not self.env['res.partner'].search([(
                'id', '=', self.partner_id.id)]):
            self.partner_id = False
        if self.partner_id:
            if self.partner_id.company_id != self.company_id:
                self.partner_id = False
            res = self.onchange_partner_id()

        if self.team_id and self.team_id.company_id != self.company_id:
            self.team_id = False
        if self.user_id and self.user_id.company_id != self.company_id and self.user_id.company_id not in self.user_id.company_ids:
            self.user_id = False
        if self.partner_id:
            self.fiscal_position_id = self.env['account.fiscal.position'].\
                get_fiscal_position(self.partner_id.id,
                                    self.partner_shipping_id.id)
        self.pricelist_id = False
        self.project_id = False
        self.related_project_id = False
        self.invoice_ids = False
        self.payment_term_id = False
        return res

    @api.model
    def default_get(self, fields):
        rec = super(SaleOrder, self).default_get(fields)
        team = self.env['crm.team']._get_default_team_id()
        if team.company_id:
            rec.update({
                'company_id': team.company_id.id})
        return rec

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a Sales Order.
        This method may be overridden to implement custom invoice generation
        (making sure to call super() to establish a clean extension chain).
        """
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        self.ensure_one()
        journal_id = self.env['account.journal'].search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_id.id)], limit=1)
        if not journal_id:
            raise UserError(_('Please define an accounting sale journal for '
                              'this company.'))
        invoice_vals['account_id'] =\
            self.with_context(force_company=self.company_id.id).\
            partner_invoice_id.property_account_receivable_id.id
        invoice_vals['fiscal_position_id'] =\
            self.fiscal_position_id.id or self.\
            with_context(force_company=self.company_id.id).partner_invoice_id.\
            property_account_position_id.id
        invoice_vals['journal_id'] = journal_id.ensure_one().id
        return invoice_vals

    @api.multi
    @api.onchange('partner_shipping_id', 'partner_id', 'company_id')
    def onchange_partner_shipping_id(self):
        """
        Trigger the change of fiscal position when the
        shipping address is modified.
        """
        self.fiscal_position_id = self.with_context(
            force_company=self.company_id.id).env[
            'account.fiscal.position'].get_fiscal_position(
            self.partner_id.id, self.partner_shipping_id.id)
        for line in self.order_line:
            line.change_company()
        return {}

    @api.multi
    @api.constrains('team_id', 'company_id')
    def _check_company_team_id(self):
        for order in self.sudo():
            if order.company_id and order.team_id.company_id and \
                    order.company_id != order.team_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Sales Team must be the same.'))
        return True

    @api.multi
    @api.constrains('partner_id', 'company_id')
    def _check_partner_company(self):
        for rec in self:
            if (rec.partner_id and rec.partner_id.company_id and
                    rec.partner_id.company_id != rec.company_id):
                raise ValidationError(_('Configuration error\n'
                                        'The Company of the Partner '
                                        'must match with that of the '
                                        'Quotation/Sales Order.'))

    @api.multi
    @api.constrains('pricelist_id', 'company_id')
    def _check_company_pricelist_id(self):
        for order in self.sudo():
            if order.company_id and order.pricelist_id.company_id and \
                    order.company_id != order.pricelist_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Pricelist must be the same.'))
        return True

    @api.multi
    @api.constrains('project_id', 'company_id')
    def _check_company_project_id(self):
        for order in self.sudo():
            if order.company_id and order.project_id.company_id and \
                    order.company_id != order.project_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Project must be the same.'))
        return True

    @api.multi
    @api.constrains('related_project_id', 'company_id')
    def _check_company_related_project_id(self):
        for order in self.sudo():
            if order.company_id and order.related_project_id.company_id and \
                    order.company_id != order.related_project_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Analytic Account must be the same.'))
        return True

    @api.multi
    @api.constrains('invoice_ids', 'company_id')
    def _check_company_invoice_ids(self):
        for order in self.sudo():
            for account_invoice in order.invoice_ids:
                if order.company_id and account_invoice.company_id and \
                        order.company_id != account_invoice.company_id:
                    raise ValidationError(
                        _('The Company in the Sales Order and in '
                          'Invoice must be the same.'))
        return True

    @api.multi
    @api.constrains('payment_term_id', 'company_id')
    def _check_company_payment_term_id(self):
        for order in self.sudo():
            if order.company_id and order.payment_term_id.company_id and \
                    order.company_id != order.payment_term_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Payment Term must be the same.'))
        return True

    @api.multi
    @api.constrains('user_id', 'company_id')
    def _check_sales_user_company(self):
        for rec in self:
            if (rec.user_id and rec.user_id.company_id and
                    rec.user_id.company_id != rec.company_id and
                    rec.company_id not in rec.user_id.company_ids):
                raise ValidationError(_('Configuration error\n'
                                        'The Company of the salesperson '
                                        'must match with that of the '
                                        'Quotation/Sales Order.'))

    @api.multi
    @api.constrains('fiscal_position_id', 'company_id')
    def _check_company_fiscal_position_id(self):
        for order in self.sudo():
            if order.company_id and order.fiscal_position_id.company_id and \
                    order.company_id != order.fiscal_position_id.company_id:
                raise ValidationError(
                    _('The Company in the Sales Order and in '
                      'Fiscal Position must be the same.'))
        return True

    @api.constrains('company_id')
    def _check_company_id(self):
        pass


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('company_id')
    def change_company(self):
        self._compute_tax_id()

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line
        for a Sales Order Line.
        :param qty: float quantity to invoice
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        self.ensure_one()
        account = self.with_context(force_company=self.company_id.id).\
            product_id.property_account_income_id or self.\
            with_context(force_company=self.company_id.id).product_id.\
            categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product:'
                              '"%s" (id:%d)  - or for its category: "%s".'
                              ) % (self.product_id.name, self.product_id.id,
                                   self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.\
            with_context(force_company=self.company_id.id).\
            order_id.partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
        res['account_id'] = account.id
        return res

    @api.multi
    @api.constrains('tax_id', 'company_id')
    def _check_tax_company(self):
        for rec in self.sudo():
            if (rec.tax_id.company_id and rec.tax_id.company_id !=
                    rec.company_id):
                raise ValidationError(_('Configuration error\n'
                                        'The Company of the tax %s '
                                        'must match with that of the '
                                        'Quotation/Sales Order.') %
                                      rec.tax_id.name)

    @api.multi
    @api.constrains('product_id', 'company_id')
    def _check_product_company(self):
        for rec in self.sudo():
            if (rec.product_id.company_id and
                    rec.product_id.company_id != rec.company_id):
                raise ValidationError(_('Configuration error\n'
                                        'The Company of the product '
                                        'must match with that of the '
                                        'Sales Order line %s.') % rec.name)
