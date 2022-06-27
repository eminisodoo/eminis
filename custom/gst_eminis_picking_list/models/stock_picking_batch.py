from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'


    def _run_stock_picking_batch(self):
        sp_batch_obj = self.env["stock.picking.batch"]
        picking_type_id = self.env.user.company_id.picking_type_id.id
        stock_pickings = self.env["stock.picking"].search([('state','in',['assigned']),
                                                            ('picking_type_id','=',picking_type_id),
                                                            ('batch_id','=',False)])
        qty = 0
        picking_lines = []
        sp_qty = len(stock_pickings)
        for sp in stock_pickings:
            sp_qty -= 1
            qty += len(sp.move_line_ids_without_package)
            if qty <= 40:
                picking_lines.append(sp)
            else:
                if picking_lines:
                    sp_batch_obj.create({
                                'picking_type_id': picking_type_id,
                                'picking_ids': [(4, pl.id) for pl in picking_lines]
                                })
                qty = len(sp.move_line_ids_without_package)
                picking_lines = [sp]
            if sp_qty == 0:
                sp_batch_obj.create({
                        'picking_type_id': picking_type_id,
                        'picking_ids': [(4, pl.id) for pl in picking_lines]
                        })
        return True

    def _get_report_filename(self):
        self.ensure_one()
        return 'PickingList-%s' % (fields.Date.today().strftime('%d-%m-%Y'))
