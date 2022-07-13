{
    "name": "GST E-minis Product",
    "version": "15.0.1",
    "category": "Sales/Sales",
    "author": "Guadaltech Soluciones Tecnológicas S.L.",
    "website": "http://www.guadaltech.es",
    "license": "LGPL-3",
    "description":
        """
        * Add fields in the product form that allow knowing if it is in pre-order
        * Add field to indicate the label with the purchase option:
            - To Buy: means that there is stock available.
            - On way: there is no stock but there is a confirmed purchase receipt.
            - Pre-order: no stock, no delivery note. But the amount that can be purchased is indicated.
            - Reserve: there is no stock or delivery notes. In the event that it was pre-ordered and the quantities have been sold out, it must also be shown as a reserve.
        """,
    "depends": [
        "product",
    ],
    "data": [
        "views/product_template_views.xml",
    ]
}
