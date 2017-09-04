# -*- coding: utf-8 -*-
{
    'name': "cine",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cine.xml',
        'views/sala.xml',
        'views/sessio.xml',
        'views/pelicula.xml',
        'views/butaca.xml',
        'views/entrada.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/salas.xml',
        'demo/butaques.xml',  'demo/pelis.xml', 'demo/sessions.xml', 'demo/entrades.xml',

    ],
}
