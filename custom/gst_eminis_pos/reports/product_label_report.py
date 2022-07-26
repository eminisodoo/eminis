# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import _, models, api
from odoo.exceptions import UserError, ValidationError


class ReportProductTemplateLabelEminis(models.AbstractModel):
    _inherit = 'report.gst_eminis_product.report_producttemplatelabel_eminis'


    def _prepare_data(self, data):
        # change product ids by actual product object to get access to fields in xml template
        # we needed to pass ids because reports only accepts native python types (int, float, strings, ...)
        total = 0
        quantity_by_product = defaultdict(list)

        if self._context.get('send_by_pos'):
            products = self.env['product.template'].search([('changed_price','=',True),('available_in_pos','=',True)])
            q = 1
            for p in products:
                quantity_by_product[p].append((p.barcode, q))
                total += q

            return {
                'quantity': quantity_by_product,
                'rows': 1,
                'columns': 1,
                'page_numbers': (total - 1) // 2,
                'price_included': False,
            }
        else:
            if data.get('active_model') == 'product.template':
                Product = self.env['product.template'].with_context(display_default_code=False)
            elif data.get('active_model') == 'product.product':
                Product = self.env['product.product'].with_context(display_default_code=False)
            else:
                raise UserError(_('Product model not defined, Please contact your administrator.'))

            for p, q in data.get('quantity_by_product').items():
                product = Product.browse(int(p))
                quantity_by_product[product].append((product.barcode, q))
                total += q

            layout_wizard = self.env['product.label.layout'].browse(data.get('layout_wizard'))
            if not layout_wizard:
                return {}

            return {
                'quantity': quantity_by_product,
                'rows': layout_wizard.rows,
                'columns': layout_wizard.columns,
                'page_numbers': (total - 1) // (layout_wizard.rows * layout_wizard.columns) + 1,
                'price_included': data.get('price_included'),
                'extra_html': layout_wizard.extra_html,
            }
