from odoo import _, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    location_code = fields.Char('Location code')
