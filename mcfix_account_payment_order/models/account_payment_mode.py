from odoo import models, api


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    @api.onchange('company_id')
    def company_id_change(self):
        super(AccountPaymentMode, self).company_id_change()
        self.payment_method_id_change()

    @api.onchange('payment_method_id')
    def payment_method_id_change(self):
        if self.payment_method_id:
            ajo = self.env['account.journal']
            aj_ids = []
            if self.payment_method_id.payment_type == 'outbound':
                aj_ids = ajo.search([
                    ('type', 'in', ('purchase_refund', 'purchase')), ('company_id', '=', self.company_id.id)]).ids
            elif self.payment_method_id.payment_type == 'inbound':
                aj_ids = ajo.search([
                    ('type', 'in', ('sale_refund', 'sale')), ('company_id', '=', self.company_id.id)]).ids
            self.default_journal_ids = [(6, 0, aj_ids)]
