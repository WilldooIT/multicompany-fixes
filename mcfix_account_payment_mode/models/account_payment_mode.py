from odoo import models, api


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    @api.onchange('company_id')
    def company_id_change(self):
        self.variable_journal_ids = False
        self.fixed_journal_id = False
