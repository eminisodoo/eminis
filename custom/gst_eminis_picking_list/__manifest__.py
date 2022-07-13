{
    "name": "GST E-minis Picking List",
    "version": "15.0.1",
    "category": "Inventory/Inventory",
    "author": "Guadaltech Soluciones Tecnológicas S.L.",
    "website": "http://www.guadaltech.es",
    "license": "LGPL-3",
    "description":
        """
        Adding the Picking list report and the default Operation type configuration to stock picking batch.
        """,
    "depends": [
        "stock_picking_batch","report_xlsx"
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_location.xml",
        "data/ir_cron_data.xml",
        "reports/picking_list_report_xlsx.xml",
    ]
}
