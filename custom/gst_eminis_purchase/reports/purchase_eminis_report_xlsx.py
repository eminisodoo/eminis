from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class PurchaseEminisXlsx(models.AbstractModel):
    _name = 'report.gst_eminis_purchase.purchase_eminis_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, purchaselist):
        sheet = workbook.add_worksheet(_('Purchase E-minis'))
        purchase_data = self._prepare_report_data()

        header_format = workbook.add_format({'border': 1, 'bold': 1, 'align': 'left'})
        body_gral_format = workbook.add_format({'align': 'left'})
        kpi_format = workbook.add_format({'align': 'right'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center'})
        number_format = workbook.add_format({'num_format': '0.00', 'align': 'right'})

        self._render_content_report(sheet, workbook, header_format, body_gral_format, date_format, number_format, kpi_format, purchase_data)

    def _render_content_report(self, sheet, workbook, header_format, body_gral_format, date_format, number_format, kpi_format, purchase_data):
        section_row = 0
        section_header_col = 0

        # 1. render section header .....................................................................................
        col_name = [_('MODEL'),_('NAME'),_('STOCK'),_('V.60'),_('SALES'),_('PVP'),_('Last Sale'),
                    _('Last Entry'),_('Index 1'),_('Register'),_('Discontinued'),_('Hidden')]
        for col in col_name:
            sheet.write(section_row, section_header_col, col, header_format)
            section_header_col +=1

        # 2. render section body .......................................................................................
        for line in purchase_data:
            section_row += 1
            section_col = 0
            # Product Default Code
            sheet.write(section_row, section_col, line['default_code'].upper() if line['default_code'] else '', body_gral_format)
            # Product Name
            sheet.write(section_row, section_col+1, line['product_name'], body_gral_format)
            # Stock qty
            stock_qty_format = workbook.add_format({'align': 'left','bg_color': line['color_stock']})
            sheet.write(section_row, section_col+2, line['stock_qty'], stock_qty_format)
            # V.60 qty
            sheet.write(section_row, section_col+3, line['v60_qty'], body_gral_format)
            # Total Sales
            sheet.write(section_row, section_col+4, line['sales_qty'], body_gral_format)
            # product price (PVP)
            sheet.write(section_row, section_col+5, line['list_price'], number_format)
            # Last sale
            sheet.write(section_row, section_col+6, line['last_sale'], date_format)
            # Last entry(purchase)
            sheet.write(section_row, section_col+7, line['last_entry'], date_format)
            # KPI Index 1
            sheet.write(section_row, section_col+8, line['kpi_index1'], kpi_format)
            # Product create date
            sheet.write(section_row, section_col+9, line['create_date'], date_format)
            # Discontinued (Archived)
            sheet.write(section_row, section_col+10, line['discontinued'], body_gral_format)
            # Hidden
            sheet.write(section_row, section_col+11, line['hidden'], body_gral_format)

        return True


    def _prepare_report_data(self):
        query = self._get_query()
        self._cr.execute(query)
        results = self._cr.dictfetchall()
        for line in results:
            product = self.env['product.product'].browse(line['product_id'])

            # Stock qty
            stock_loc = self.env['stock.location']
            stock_quant = self.env['stock.quant']
            ac = stock_loc.search([('complete_name','=','AC/Stock')])
            tll = stock_loc.search([('complete_name','=','TLL/Stock')])
            tm = stock_loc.search([('complete_name','=','TM/Stock')])
            qty_ac = stock_quant.search([('product_id','=',line['product_id']),('location_id','=',ac.id)])
            qty_tll = stock_quant.search([('product_id','=',line['product_id']),('location_id','=',tll.id)])
            qty_tm = stock_quant.search([('product_id','=',line['product_id']),('location_id','=',tm.id)])

            line['stock_qty'] = qty_ac.quantity + qty_tll.quantity + qty_tm.quantity

            ### Calculate Offer (20%)
            percent = product.list_price * 0.2

            # V.60 qty
            filter_date = fields.Datetime.now() - relativedelta(days=60)
            so_v60 = self.env['sale.order.line'].search([('product_id','=',line['product_id'])])\
                .filtered(lambda line: line.order_id.date_order >= filter_date)
            po_v60 = self.env['pos.order.line'].search([('product_id','=',line['product_id'])])\
                .filtered(lambda line: line.order_id.date_order >= filter_date)

            qty_with_offer_v60 = 0
            qty_without_offer_v60 = 0
            for sol in so_v60:
                if sol.discount > 0:
                    if (sol.price_unit * sol.discount)/100 >= percent:
                        qty_with_offer_v60 += 1
                    else:
                        qty_without_offer_v60 += 1
                elif sol.price_unit <= product.list_price - percent:
                    qty_with_offer_v60 += 1
                else:
                    qty_without_offer_v60 += 1
            for sol in po_v60:
                if sol.discount > 0:
                    if (sol.price_unit * sol.discount)/100 >= percent:
                        qty_with_offer_v60 += 1
                    else:
                        qty_without_offer_v60 += 1
                elif sol.price_unit <= product.list_price - percent:
                    qty_with_offer_v60 += 1
                else:
                    qty_without_offer_v60 += 1

            if qty_with_offer_v60 != 0:
                line['v60_qty'] = str(qty_without_offer_v60) + ' (Of:' + str(qty_with_offer_v60) + ')'
            else:
                line['v60_qty'] = str(qty_without_offer_v60)

            # Total Sales
            filter_date = fields.Datetime.now()
            so_sales = self.env['sale.order.line'].search([('product_id','=',line['product_id'])])\
                .filtered(lambda line: line.order_id.date_order <= filter_date)
            po_sales = self.env['pos.order.line'].search([('product_id','=',line['product_id'])])\
                .filtered(lambda line: line.order_id.date_order <= filter_date)

            qty_with_offer = 0
            qty_without_offer = 0
            for sol in so_sales:
                if sol.discount > 0:
                    if (sol.price_unit * sol.discount)/100 >= percent:
                        qty_with_offer += 1
                    else:
                        qty_without_offer += 1
                elif sol.price_unit <= product.list_price - percent:
                    qty_with_offer += 1
                else:
                    qty_without_offer += 1
            for sol in po_sales:
                if sol.discount > 0:
                    if (sol.price_unit * sol.discount)/100 >= percent:
                        qty_with_offer += 1
                    else:
                        qty_without_offer += 1
                elif sol.price_unit <= product.list_price - percent:
                    qty_with_offer += 1
                else:
                    qty_without_offer += 1

            if qty_with_offer != 0:
                line['sales_qty'] = str(qty_without_offer) + ' (Of:' + str(qty_with_offer) + ')'
            else:
                line['sales_qty'] = str(qty_without_offer)

            # Last sale
            so_line = self.env['sale.order.line'].search([('product_id','=',line['product_id'])],
                                                            order='create_date desc', limit=1)

            line['last_sale'] = so_line.order_id.date_order.date() if so_line.order_id.date_order else ''

            # Last entry(purchase)
            po_line = self.env['purchase.order.line'].search([('product_id','=',line['product_id'])],
                                                            order='create_date desc', limit=1)

            line['last_entry'] = po_line.order_id.date_planned.date() if po_line.order_id.date_planned else ''

            # Discontinued (Archived)
            line['discontinued'] = _('Discontinued') if not product.active else ''

            # KPI Index 1
            days = (so_line.order_id.date_order - po_line.order_id.date_planned).days if so_line.order_id.date_order and po_line.order_id.date_planned else ''
            if days != '':
                so_lines = self.env['sale.order.line'].search([('product_id','=',line['product_id'])])\
                    .filtered(lambda line: po_line.order_id.date_planned <= line.order_id.date_order <= so_line.order_id.date_order)

                sales = '00'
                if so_lines:
                    sales = '0' + str(len(so_lines)) if len(so_lines) < 10 else str(len(so_lines))

                line['kpi_index1'] = str(days) + ',' + sales
            else:
                line['kpi_index1'] = days

            # Hidden
            hidden = ''
            order_point = self.env['stock.warehouse.orderpoint'].search([('product_id','=',product.id),
                                                                         ('product_min_qty','=',-1),
                                                                         ('product_max_qty','=',0)])

            if line['stock_qty'] > 0 >= (qty_with_offer_v60 + qty_without_offer_v60):
                hidden = _('HIDDEN 1')
            elif line['stock_qty'] >= 0 and order_point:
                hidden = _('HIDDEN 2')
            #elif line['stock_qty'] <= 0 and (qty_with_offer_v60 + qty_without_offer_v60) <= 0 and line['discontinued'] != '':
            elif line['stock_qty'] >= 0 and line['discontinued'] != '':
                hidden = _('HIDDEN 3')
            elif line['stock_qty'] > 0 and line['stock_qty'] >= 3 * (qty_with_offer_v60 + qty_without_offer_v60):
                hidden = _('HIDDEN 4')

            line['hidden'] = hidden

            # Set Stock Color
            color = '#ffffff'
            if line['stock_qty'] < (qty_with_offer_v60 + qty_without_offer_v60):
                color = '#f81200'
            elif line['stock_qty'] == (qty_with_offer_v60 + qty_without_offer_v60) and line['stock_qty'] == 0:
                color = '#fdcb96'
            elif line['stock_qty'] == (qty_with_offer_v60 + qty_without_offer_v60) and line['stock_qty'] != 0:
                color = '#fa9a00'
            elif line['stock_qty'] < (qty_with_offer + qty_without_offer):
                color = '#9acdfd'

            line['color_stock'] = color

        return results


    def _get_query(self):
        return '%s %s %s' % (self._select(), self._from(), self._group_by())

    def _select(self):
        select_str = """
            SELECT
                p.id as product_id,
                t.name as product_name,
                p.default_code,
                date(p.create_date) as create_date,
                t.list_price
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
            product_product p
                left join product_template t on (p.product_tmpl_id=t.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                p.id,
                t.name,
                p.default_code,
                p.create_date,
                t.list_price
        """
        return group_by_str


