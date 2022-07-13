# -*- coding: utf-8 -*-
from odoo import models, fields, api


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
                                ], default='to_buy', string="Purchase Tags")
