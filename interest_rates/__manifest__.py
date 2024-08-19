# Copyright 2020 Agrista (https://agrista.com)
{
    'name': 'Interest Rates',
    'version': '17.0.1.0.1',
    'author': 'Agrista',
    'website': 'https://github.com/agrista/odoo-interest-rates',
    'license': 'AGPL-3',
    'category': 'Financial Management/Configuration',
    'summary': 'Update the lending rate / interest rate',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/interest.xml',
        'views/interest_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
}
