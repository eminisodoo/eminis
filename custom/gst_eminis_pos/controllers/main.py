# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request, content_disposition

_logger = logging.getLogger(__name__)


class PosController(http.Controller):


    @http.route('/pos/product_template_label_eminis_report/download', type='http', auth='user')
    def print_product_template_label_eminis(self, **kw):
        r = request.env['report.gst_eminis_product.report_producttemplatelabel_eminis']
        pdf, file_extension = request.env.ref('gst_eminis_pos.product_template_label_eminis_report').with_context(send_by_pos=True)._render_qweb_pdf(r)
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf)),
                          ('Content-Disposition', content_disposition(_('Product Labels.%s' % file_extension)))]
        return request.make_response(pdf, headers=pdfhttpheaders)
