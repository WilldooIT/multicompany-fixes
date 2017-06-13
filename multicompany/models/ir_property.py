from odoo import models, api


class Property(models.Model):
    _inherit = 'ir.property'

    @api.model
    def get_calculated(self, name, model, res_id=False):
        value = self.get(name, model, res_id)
        if value:
            return value
        value = self.get(name, model)
        if value:
            return value
        return False

    @api.model
    def set_default(self, name, model, default_value):
        """ Assign the property field `name` for the default record of model `model`
                    with `default_value` (dictionary mapping record ids to their value)
                    for company 'company_id'.
                """
        def clean(val):
            return val.id if isinstance(val, models.BaseModel) else val

        # retrieve the properties corresponding to the given record ids
        self._cr.execute("SELECT id FROM ir_model_fields WHERE name=%s AND model=%s", (name, model))
        field_id = self._cr.fetchone()[0]
        company_id = self.env.context.get('force_company') or self.env['res.company']._company_default_get(model,
                                                                                                           field_id).id

        props = self.search([
            ('fields_id', '=', field_id),
            ('company_id', '=', company_id),
            ('res_id', '=', False),
        ])
        value = clean(default_value)
        # modify existing properties
        for prop in props:

            if value != clean(prop.get_by_record()):
                prop.write({'value': value})

        if not props:
            self.create({
                'fields_id': field_id,
                'company_id': company_id,
                'res_id': False,
                'name': name,
                'value': value,
                'type': self.env[model]._fields[name].type,
            })
