# -*- coding: utf-8 -*-
{
    'name': "efulrental",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'installable': True,
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/slot_waktu_pengambilan.xml',
        'views/menu.xml',
        'views/pengambilan_views.xml',
        'wizard/booking_form.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/booking_views.xml',        
        'views/penyewa_views.xml',
        'views/staff_views.xml',
        'views/stokmobil_views.xml',
        'report/report.xml',
        'report/booking_report_template.xml',
        'report/billing_report.xml',
        'views/brand_ambassador_views.xml',
        'views/partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
