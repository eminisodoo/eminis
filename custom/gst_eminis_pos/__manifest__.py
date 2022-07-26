{
    "name": "GST E-minis Pos",
    "version": "15.0.1",
    "category": "Sales/Point of Sale",
    "author": "Guadaltech Soluciones Tecnológicas S.L.",
    "website": "http://www.guadaltech.es",
    "license": "LGPL-3",
    "description":
        """
        Adding the following features to the PoS interface for shops:
        * Show alert of products with modified price.
        * Print product labels with modified price.
        """,
    "depends": [
        "gst_eminis_product","point_of_sale"
    ],
    "data": [
        "reports/point_of_sale_report.xml",
    ],

    "assets": {
        "web.assets_qweb": [
            'gst_eminis_pos/static/src/xml/**/*',
        ],
        'point_of_sale.assets': [
            'gst_eminis_pos/static/src/css/pos.css',
            'gst_eminis_pos/static/src/js/**/*.js',
        ],
    },
}
