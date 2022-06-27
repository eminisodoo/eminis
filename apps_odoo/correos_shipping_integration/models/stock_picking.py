from odoo import models, fields, api


class CorreosTrackingNumber(models.Model):
    _inherit = 'stock.picking'

    correos_tracking_id = fields.Char(string="Correos CodManifiesto", copy=False,help="CodManifiesto")
