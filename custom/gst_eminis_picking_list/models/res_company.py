from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    picking_type_id = fields.Many2one("stock.picking.type", string="Operation Type")


