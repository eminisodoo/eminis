# -*- coding: utf-8 -*-

{   
    'name': 'Correos Express Integration ',
    'summary': """Our Odoo to CORREOS EXPRESS Shipping Integration will help you to connect your Odoo with CORREOS EXPRESS (www.correosexpress.com).You will be able to automatically submit order information from stock picking and get Shipping label and
Order Tracking number.We also have integrations with: Correos, DHL Parcel, DHL Express, Fedex, UPS, GLS (ASM), USPS, Stamps.com.""",

    'description': """

Features
--------

Our Odoo to CORREOS EXPRESS Shipping Integration will help you to connect your Odoo with CORREOS EXPRESS (www.correosexpress.com).

You will be able to automatically submit order information from stock picking and get Shipping label and
Order Tracking number.

NOTICE: this module does NOT connect with Correos  (www.correos.es). Please check our other modules.

We also have integrations with: Correos, DHL Parcel, DHL Express, Fedex, UPS, GLS (ASM), USPS, Stamps.com.
        """,

    'category': 'Stock',
    'author': "Vraja Technologies",
    'version': '14.0.0.0.0',
    'depends': ['delivery'],
    'data': [
            'views/res_company.xml',
        'views/delivery_carrier_view.xml',
        'views/stock_picking_view.xml',
             ],
    'images': ['static/description/correos_express.png'],
    # 'images': ['static/description/christmas.gif'],
    'maintainer': 'Vraja Technologies',
    'website':'www.vrajatechnologies.com',
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'live_test_url': 'http://www.vrajatechnologies.com/contactus',
    'price': '279',
    'currency': 'EUR',
    'license': 'OPL-1',
}

# version changelog
# 13.0.18.06.2021 Add receiver email address
