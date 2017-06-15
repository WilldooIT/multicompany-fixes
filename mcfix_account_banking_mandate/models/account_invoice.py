# -*- coding: utf-8 -*-
# © 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def check_mandate(self):
        if (
            self.type == 'out_invoice' and
            self.payment_mode_id.payment_type == 'inbound' and
            self.payment_mode_id.payment_method_id.mandate_required and
            self.commercial_partner_id
        ):
            mandates = self.env['account.banking.mandate'].search([
                ('state', '=', 'valid'),
                ('company_id', '=', self.company_id.id),
                ('partner_id', '=', self.commercial_partner_id.id),
            ])
            if mandates:
                self.mandate_id = mandates[0]
        else:
            self.mandate_id = False

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        """Select by default the first valid mandate of the partner"""
        super(AccountInvoice, self)._onchange_partner_id()
        self.check_mandate()

    @api.onchange('payment_mode_id')
    def payment_mode_id_change(self):
        super(AccountInvoice, self).payment_mode_id_change()
        self.check_mandate()
