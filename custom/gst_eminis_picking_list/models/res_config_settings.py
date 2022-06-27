from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    picking_type_id = fields.Many2one("stock.picking.type", related="company_id.picking_type_id", readonly=False)

    @api.onchange("module_stock_picking_batch")
    def _onchange_stock_picking_batch(self):
        if self.module_stock_picking_batch:
            if not self.picking_type_id:
                warehouse = self.env["stock.warehouse"].search([('code','=','AC')], limit=1)
                picking_type = self.env["stock.picking.type"].search([('sequence_code','=','PICK'),('warehouse_id','in',warehouse.ids)], limit=1)
                self.picking_type_id = picking_type.id
        else:
            self.picking_type_id = False

