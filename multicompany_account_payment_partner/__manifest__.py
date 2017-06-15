# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Purchase',
    'version': '1',
    'summary': 'Creu Blanca configuration',
    'author': 'Creu Blanca',
    'sequence': 30,
    'description': "",
    'category': 'Creu Blanca',
    'website': 'http://www.creublanca.es',
    'depends': ['account_payment_partner', 'multicompany_account'],
    'data': [
        'views/partner.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
