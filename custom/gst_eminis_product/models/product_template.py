# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pre_order = fields.Boolean('Pre Order')
    estimated_date = fields.Date(string='Estimated Date', index=True)
    estimated_qty = fields.Float(string='Estimated Qty')
    purchase_tags = fields.Selection([
                                ('to_buy', 'To Buy'),
                                ('on_way', 'On Way'),
                                ('pre_order', 'Pre Order'),
                                ('reserve', 'Reserve'),
                                ], string="Purchase Tags", compute='_compute_purchase_tags')
    previous_price = fields.Float('Previous Price', digits='Product Price')
    offer_price = fields.Float('Offer Price', digits='Product Price')
    changed_price = fields.Boolean('Changed Price', default=False)
    changed_date = fields.Date(string='Changed Date', index=True)


    def _compute_purchase_tags(self):
        for prod in self:
            stock_loc = self.env['stock.location']
            stock_quant = self.env['stock.quant']
            ac = stock_loc.search([('complete_name','=','AC/Stock')])
            tll = stock_loc.search([('complete_name','=','TLL/Stock')])
            tm = stock_loc.search([('complete_name','=','TM/Stock')])
            qty_ac = stock_quant.search([('product_id','=',prod.id),('location_id','=',ac.id)])
            qty_tll = stock_quant.search([('product_id','=',prod.id),('location_id','=',tll.id)])
            qty_tm = stock_quant.search([('product_id','=',prod.id),('location_id','=',tm.id)])

            total_stock_qty = qty_ac.quantity + qty_tll.quantity + qty_tm.quantity

            picking_type_ids = self.env['stock.picking.type'].search([('code','=','incoming')])
            picking_ids = self.env['stock.picking'].search([('picking_type_id','in',picking_type_ids.ids),('state','=','confirmed')])
            exist_pick = False
            for pick in picking_ids:
                lines = pick.move_line_ids_without_package.filtered(lambda ml: ml.product_id.id == prod.id)
                if lines:
                    exist_pick = True
                    break

            if total_stock_qty > 0:
                prod.purchase_tags = 'to_buy'
            elif exist_pick and total_stock_qty <= 0:
                prod.purchase_tags = 'on_way'
            elif not exist_pick and total_stock_qty <= 0:
                if prod.pre_order and prod.estimated_qty > 0 and prod.estimated_qty >= abs(prod.virtual_available):
                    prod.purchase_tags = 'pre_order'
                #elif prod.estimated_qty < abs(prod.virtual_available):
                else:
                    prod.purchase_tags = 'reserve'


    def _update_changed_price(self):
        product_ids = self.env['product.template'].search([])
        for prod in product_ids:
            new_date = fields.date.today() - relativedelta(days=60)
            if prod.changed_date:
                if new_date > prod.changed_date:
                    prod.write({'changed_price': False})


    def write(self, vals):
        if 'list_price' in vals:
            product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
            pricelist_item = self.env['product.pricelist.item'].search([('product_tmpl_id','=',self.id),
                                                                       ('compute_price','=','percentage'),
                                                                       ('percent_price','=',20)], limit=1)
            values = self._get_combination_info(product_id=product.id, pricelist=pricelist_item.pricelist_id)

            if values['price'] != values['list_price']:
                vals['previous_price'] = vals['list_price']
                vals['offer_price'] = values['price']
            else:
                vals['previous_price'] = self.list_price
                vals['offer_price'] = vals['list_price']

            vals['changed_price'] = True
            vals['changed_date'] = fields.date.today()

        return super(ProductTemplate, self).write(vals)
