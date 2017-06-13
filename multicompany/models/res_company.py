from odoo import models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.one
    def set_default(self, field, model, value):
        self.env['ir.property'].with_context(force_company=self.id).set_default(field, model, value)
