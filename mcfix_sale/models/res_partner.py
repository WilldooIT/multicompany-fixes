# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    relevant_company_id = fields.Many2one('res.company', compute='_compute_relevant_company', search='_search_relevant_company')

    @api.multi
    def _compute_relevant_company(self):
        for partner in self:
            partner.relevant_company_id = partner.company_id

    @api.model
    def _search_relevant_company(self, operator, value):
        assert operator == 'child_of'
        assert isinstance(value, (list, tuple))
        res = self.search([('company_id', operator, value)])

        users = self.env['res.users'].search([('company_ids', operator, value)])
        res |= users.mapped('partner_id')

        return [('id', 'in', res.ids)]

    @api.multi
    @api.constrains('company_id')
    def _check_sales_order_company(self):
        for rec in self:
            if rec.company_id:
                order_partner_id = self.env['sale.order'].\
                    search([('partner_id', '=', rec.id),
                            ('company_id', '!=', False),
                            ('company_id', '!=', rec.company_id.id)], limit=1)
                order_partner_shipping_id = self.env['sale.order'].search(
                    [('partner_shipping_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                order_partner_invoice_id = self.env['sale.order'].search(
                    [('partner_invoice_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if order_partner_id or order_partner_shipping_id or \
                        order_partner_invoice_id:
                    raise ValidationError(_('Sales Order already exists '
                                            'referencing this partner in '
                                            'other companies.'))
