# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Product',
    'version': '1',
    'summary': 'Creu Blanca configuration',
    'author': 'Creu Blanca',
    'sequence': 30,
    'description': "",
    'category': 'Creu Blanca',
    'website': 'http://www.creublanca.es',
    'depends': ['product', 'multicompany'],
    'data': [
        'views/product.xml',
        'views/product_category.xml',
        'views/res_company_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
