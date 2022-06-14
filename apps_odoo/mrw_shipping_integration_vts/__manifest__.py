# -*- coding: utf-8 -*-pack
{
    # App information
    'name': 'MRW Shipping Integration',
    'category': 'Website',
    'version': '15.0.1',
    'summary': """""",
    'description': """Integrate & Manage MRW shipping operations from Odoo by using Odoo MRW Integration.Export Order While Validate Delivery Order.Import Tracking From MRW to odoo.Generate Label in odoo.We are providing following modules odoo shipping connector,gls,mrw,colissimo,dbschenker.""",
    'depends': ['delivery'],
    'live_test_url': 'https://www.vrajatechnologies.com/contactus',
    'data': ['view/res_company_view.xml',
             'view/delivery_carrier_view.xml',
             'view/stock_picking_view.xml'],
    'images': ['static/description/Cover.jpg'],
    'author': 'Vraja Technologies',
    'maintainer': 'Vraja Technologies',
    'website': 'https://www.vrajatechnologies.com',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': "279",
    'currency': 'EUR',
    'license': 'OPL-1',
    "cloc_exclude": [
        "./**/*",
    ]
}
# version changelog
# 14.0.11.02.21 initial module
# 14.0.25.10.21 Change version log for manage erp
# 14.0.05.04.22 check receiver street2 field have number value or not using regular expression
# 15.0.1 Changing model product_packaging to stock_package_type for new odoo version
