# -*- coding: utf-8 -*-

{   
    'name': 'Correos Integration For Spain',
    'category': 'Website',
    'author': "Vraja Technologies",
    'version': '14.0.28.10.2021',
    'summary': """""",
    'description': """

Features
--------

Our Odoo to CORREOS Shipping Integration will help you to connect your Odoo with CORREOS (www.correos.com).

You will be able to automatically submit order information from stock picking and get Shipping label and
Order Tracking number.

NOTICE: this module does NOT connect with Correos Express (www.correosexpress.es). Please check our other modules.

We also have integrations with: Correos, DHL Parcel, DHL Express, Fedex, UPS, GLS (ASM), USPS, Stamps.com, 

Shipstation, Bigcommerce, Easyship, Amazon shipping, Sendcloud, eBay, Shopify.
        """,
    'depends': ['delivery'],
    'live_test_url': 'https://www.vrajatechnologies.com/contactus',
    'data': [
            'views/res_company.xml',
            'views/delivery_carrier_view.xml',
            'views/correos_stock_picking_view.xml',
             ],
    'images': ['static/description/correios.jpg'],

    'maintainer': 'Vraja Technologies',
    'website':'https://www.vrajatechnologies.com',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '279',
    'currency': 'EUR',
    'license': 'OPL-1',
}

# 14.0.28.10.2021 Latest version of the app