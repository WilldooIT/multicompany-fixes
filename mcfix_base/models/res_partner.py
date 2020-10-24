# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        res = []
        names = super(ResPartner, self).name_get()
        multicompany_group = self.env.ref('base.group_multi_company')
        if not self.env.context.get('show_res_company', True) or multicompany_group not in self.env.user.groups_id:
            return names
        for name in names:
            rec = self.browse(name[0])
            name = '%s [%s]' % (name[1], rec.sudo().company_id.name) if \
                rec.company_id else name[1]
            res += [(rec.id, name)]
        return res

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None, show_res_company=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

    @api.one
    def _compute_current_company_id(self):
        self.current_company_id = self.env['res.company'].browse(
            self._context.get('force_company') or
            self.env.user.company_id.id).ensure_one()

    current_company_id = fields.Many2one(
        comodel_name='res.company',
        default=_compute_current_company_id,
        compute='_compute_current_company_id',
        store=False
    )
