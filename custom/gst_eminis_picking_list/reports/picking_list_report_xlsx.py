from odoo import api, fields, models, _


class PickingListXlsx(models.AbstractModel):
    _name = 'report.gst_eminis_picking_list.picking_list_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, pickinglist):
        sheet = workbook.add_worksheet(_('Picking List'))

        header_format = workbook.add_format({'bold': 1, 'align': 'left'})
        body_gral_format = workbook.add_format({'border': 1, 'align': 'left'})
        body_qties_format = workbook.add_format({'bold': 1, 'border': 1, 'align': 'right', 'font_size': 13})
        body_number_format = workbook.add_format({'border': 1, 'align': 'right'})
        body_stock_format = workbook.add_format({'border': 1, 'align': 'center'})

        self._get_sections(sheet, data, header_format, body_gral_format, body_number_format, body_qties_format, body_stock_format, pickinglist)

    def _get_sections(self, sheet, data, header_format, body_gral_format, body_number_format, body_qties_format, body_stock_format, pickinglist):
        section_row = 0
        section_header_col = 0
        section_space_row = 4

        for plist in pickinglist:
            section_col = 0

            # 1. render section header .................................................................................
            origin_list = ''
            qty_pickings = len(plist.picking_ids)-1
            for picking in plist.picking_ids.sorted(lambda r: r.origin):
                if picking.origin:
                    if qty_pickings != 0:
                        origin_list += picking.origin + ' / '
                    else:
                        origin_list += picking.origin
                    qty_pickings -= 1

            sheet.merge_range(
                    cell_format=header_format,
                    data=origin_list,
                    first_row=section_row,
                    first_col=section_header_col,
                    last_row=section_row,
                    last_col=section_header_col+7,
                    )

            # 2. render section body ...................................................................................
            for move in plist.move_ids.sorted(lambda r: r.location_id.location_code):
                section_row += 1
                # Product Default Code
                sheet.write(section_row, section_col, move.product_id.default_code.upper(), body_gral_format)
                # Product Name
                sheet.write(section_row, section_col+1, move.product_id.name, body_gral_format)
                # Product Uom Qty
                if move.product_uom_qty > 1:
                    if move.sale_line_id:
                        sheet.write(section_row, section_col+2, move.sale_line_id.product_uom_qty, body_qties_format)
                    elif move.purchase_line_id:
                        sheet.write(section_row, section_col+2, move.purchase_line_id.product_uom_qty, body_qties_format)
                    else:
                        sheet.write(section_row, section_col+2, move.product_uom_qty, body_qties_format)
                else:
                    if move.sale_line_id:
                        sheet.write(section_row, section_col+2, move.sale_line_id.product_uom_qty, body_number_format)
                    elif move.purchase_line_id:
                        sheet.write(section_row, section_col+2, move.purchase_line_id.product_uom_qty, body_number_format)
                    else:
                        sheet.write(section_row, section_col+2, move.product_uom_qty, body_number_format)
                # Price Unit
                if move.sale_line_id:
                    if move.sale_line_id.tax_id and move.sale_line_id.tax_id.amount == float(4):
                        sheet.write(section_row, section_col+3, str(move.sale_line_id.price_unit) + ' *', body_number_format)
                    else:
                        sheet.write(section_row, section_col+3, move.sale_line_id.price_unit, body_number_format)
                elif move.purchase_line_id:
                    if move.purchase_line_id.taxes_id and move.purchase_line_id.taxes_id.amount == float(4):
                        sheet.write(section_row, section_col+3, str(move.purchase_line_id.price_unit) + ' *', body_number_format)
                    else:
                        sheet.write(section_row, section_col+3, move.purchase_line_id.price_unit, body_number_format)
                else:
                    sheet.write(section_row, section_col+3, move.price_unit, body_number_format)
                # Origin
                sheet.write(section_row, section_col+4, move.origin if move.origin else '', body_gral_format)
                # Location
                sheet.write(section_row, section_col+5, move.location_id.display_name, body_gral_format)
                # Location code
                sheet.write(section_row, section_col+6, move.location_id.location_code, body_gral_format)

                # Stock quant
                stock_loc = self.env['stock.location']
                stock_quant = self.env['stock.quant']
                ac = stock_loc.search([('complete_name','=','AC/Stock')])
                tll = stock_loc.search([('complete_name','=','TLL/Stock')])
                tm = stock_loc.search([('complete_name','=','TM/Stock')])
                qty_ac = stock_quant.search([('product_id','=',move.product_id.id),('location_id','=',ac.id)])
                qty_tll = stock_quant.search([('product_id','=',move.product_id.id),('location_id','=',tll.id)])
                qty_tm = stock_quant.search([('product_id','=',move.product_id.id),('location_id','=',tm.id)])

                qty_vals = ''
                if qty_ac:
                    qty_vals += str(qty_ac.quantity)
                if qty_tll:
                    if qty_vals != '':
                        qty_vals += ' / '
                    qty_vals += 'L:' + str(qty_tll.quantity)
                if qty_tm:
                    if qty_vals != '':
                        qty_vals += ' / '
                    qty_vals += 'M:' + str(qty_tm.quantity)

                sheet.write(section_row, section_col+7, qty_vals , body_stock_format)

            section_row += section_space_row

        return True
