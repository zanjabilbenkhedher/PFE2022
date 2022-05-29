# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

{
    'name': 'facture',
    'version': '1.0',
    'summary': 'upload facture',
    'sequence': 10,
    'description': """""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'depends':['mail',],
    'data': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
 # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/fact_views.xml',
        'views/details_views.xml',
        'views/template.xml',
        'views/settings.xml',
        'views/profile_user.xml',
        'views/users.xml',
        'wizard/create_facture.xml',
        'views/modelActivity.xml',
        'data/sequence.xml',
        'data/sequence2.xml',
        'security/rule.xml',
        'views/menuitem.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

'qweb': [
        'static/xml/file.xml'
    ]
}