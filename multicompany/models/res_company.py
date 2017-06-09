from odoo import models, api, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.one
    def set_default(self, field, model, value, properties):
        self._cr.execute("SELECT id FROM ir_model_fields WHERE name=%s AND model=%s", (field, model))
        field_id = self._cr.fetchone()[0]
        prop = properties.search([
            ('fields_id', '=', field_id),
            ('company_id', '=', self.id),
            ('res_id', '=', False)
        ])
        if prop:
            prop.write({'value': value})
        else:
            properties.create({
                'fields_id': field_id,
                'company_id': self.id,
                'res_id': False,
                'name': field,
                'type': self.env[model]._fields[field].type,
                'value': value
            })
