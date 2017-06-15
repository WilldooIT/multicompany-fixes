# -*- coding: utf-8 -*-
# © 2014-2016 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.partner_id:
            if self.type == 'in_invoice':
                pay_mode = self.partner_id.with_context(force_company=self.company_id.id).supplier_payment_mode_id
                self.payment_mode_id = pay_mode
                if (
                        pay_mode and
                        pay_mode.payment_type == 'outbound' and
                        pay_mode.payment_method_id.bank_account_required and
                        self.commercial_partner_id.bank_ids
                ):
                    self.partner_bank_id = self.commercial_partner_id.bank_ids[0]
            elif self.type == 'out_invoice':
                pay_mode = self.partner_id.with_context(force_company=self.company_id.id).customer_payment_mode_id
                self.payment_mode_id = pay_mode
                if pay_mode and pay_mode.bank_account_link == 'fixed':
                    self.partner_bank_id = pay_mode.fixed_journal_id. \
                        bank_account_id
        else:
            self.payment_mode_id = False
            if self.type == 'in_invoice':
                self.partner_bank_id = False
        return res