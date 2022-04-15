# -*- coding: utf-8 -*-

{
    'name': 'facture',
    'version': '1.0',
    'summary': 'upload facture',
    'sequence': 10,
    'description': """""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'depends':[],
    'data': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/create_facture_views.xml',
        'views/fact_views.xml',
        'views/template.xml',
        'views/details_views.xml',
        'data/sequence.xml'


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/xml/file.xml'
    ]
}
