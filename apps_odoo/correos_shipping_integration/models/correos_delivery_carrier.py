import base64
import requests
import binascii
import logging
import xml.etree.ElementTree as etree
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from . import correos_response
_logger = logging.getLogger(__name__)


class CorreosDeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(selection_add =[("correos_vts","Correos")], ondelete={'correos_vts': 'set default'})
    correos_typelock = fields.Selection([('FP', 'FP - Postage Paid'),
                                          ('FM', 'FM - Machine franking'),
                                          ('ES', 'ES - Cash'),
                                          ('ON', 'ON - Online Payment')],string = "Typelock(Payment Type)", help = "Payment Method")
    correos_modality_delivery = fields.Selection([('ST', 'ST - Standard For The Product/ At Home'),
                                                   ('LS','LS - In Selected Branch'),
                                                   ('OR', 'OR - In The  Reference Branch Of The Addressee'),
                                                   ('CP', 'CP - CityPaq')], string="Modality Delivery(DropOfType)" ,help="Select Delivery Method")
    correos_weight_type = fields.Selection([('R', 'R - Real'),
                                            ('V', 'V - Volumetric')],
                                            string="Correos Weight Type", help="Weight Type provided by Correos",default='R')
    correos_packaging_id = fields.Many2one('stock.package.type', string="Default Package Type")
    correos_product_code = fields.Selection([('S0030','S0030 - NTERNATIONAL PRIORITY PARCEL (I)'),
                                              ('S0033','S0033 - EXPRESS PARCEL (N)'),
                                              ('S0034','S0034 - INTERNATIONAL EXPRESS PARCEL (I)'),
                                              ('S0198','S0198 - POSTAL EXPRES - POSTAL OFFICE DELIVERY'),
                                              ('S0132','S0132 - PAQ ESTANDAR - HOME DELIVERY'),
                                              ('S0133','S0133 - PAQ ESTANDAR - POSTAL OFFICE DELIVERY'),
                                              ('S0135','S0135 - REVERSE LOGISTICS PARCEL (GO AND BACK MODALITY)'),
                                              ('S0148','S0148 - REVERSE LOGISTICS PARCEL (BACK MODALITY ONLY)'),
                                              ('S0235','S0235 - PAQ PREMIUM - HOME DELIVERY'),
                                              ('S0236','S0236 - PAQ PREMIUM - POSTAL OFFICE DELIVERY'),
                                              ('S0197','S0197 - POSTAL EXPRES- REVERSE LOGISTICS'),
                                              ('S0031','S0031 - INTERNATIONAL ECONOMY PARCEL'),
                                              ('S0176','S0176 - PAQ PREMIUM - CITYPAQ DELIVERY'),
                                              ('S0178','S0178 - PAQ ESTANDAR - CITYPAQ DELIVERY'),
                                              ('S0292','S0292 - PAQ TODAY HOME DELIVERY'),
                                              ('S0293','S0293 - PAQ TODAY POSTAL OFFICE DELIVERY'),
                                              ('S2095','S2095 - PAQ TODAY CITYPAQ DELIVERY'),
                                              ('S0360','S0360 - PAQ LIGHT INTERNATIONAL(I)'),
                                              ('S0410','S0410 - PAQ ESTANDARD INTERNATIONAL'),
                                              ('S0411','S0411 - PAQ PREMIUM INTERNATIONAL')] , string="Product Code (Service Code)")


    def correos_vts_rate_shipment(self, order):
        return {'success': True, 'price': 0.0, 'error_message': False, 'warning_message': False}

    def correos_label_request_data(self, pickings=False):
        sender_id = pickings.picking_type_id and pickings.picking_type_id.warehouse_id and pickings.picking_type_id.warehouse_id.partner_id
        receiver_id = pickings.partner_id

        # check sender Address
        if not sender_id.zip or not sender_id.city or not sender_id.country_id:
            raise ValidationError("Please Define Proper Sender Address!")

        # check Receiver Address
        if not receiver_id.zip or not receiver_id.city or not receiver_id.country_id:
            raise ValidationError("Please Define Proper Recipient Address!")

        master_node1 = etree.Element('soap:Envelope')
        master_node1.attrib['xmlns:soap'] = 'http://schemas.xmlsoap.org/soap/envelope/'
        sub_master_node_1 = etree.SubElement(master_node1,'soap:Body')
        sub_master_node_2 = etree.SubElement(sub_master_node_1,'PreregistroEnvio')
        sub_master_node_2.attrib['xmlns'] = 'http://www.correos.es/iris6/services/preregistroetiquetas'
        etree.SubElement(sub_master_node_2,'fechaOperacion').text = "{}".format(self.create_date)
        etree.SubElement(sub_master_node_2,'CodEtiquetador').text = "{}".format(self.company_id and self.company_id.correos_customer_code)
        etree.SubElement(sub_master_node_2,'Care').text = ""
        etree.SubElement(sub_master_node_2,'ModDevEtiqueta').text = "{}".format(2) #Need PDF Data So directlly written 2.

        # Sender Data
        submaster_node = etree.SubElement(sub_master_node_2,'Remitente')
        root_node = etree.SubElement(submaster_node,'Identificacion')
        etree.SubElement(root_node,'Nombre').text = "{}".format(sender_id.name)
        root_node1 = etree.SubElement(submaster_node,'DatosDireccion')
        etree.SubElement(root_node1,'Direccion').text = "{}".format(sender_id.street)
        etree.SubElement(root_node1,'Localidad').text = "{}".format(sender_id.city)
        etree.SubElement(submaster_node,'CP').text = "{}".format(sender_id.zip)
        etree.SubElement(submaster_node,'Telefonocontacto').text = "{}".format(sender_id.phone)
        etree.SubElement(submaster_node,"Email").text ="{}".format(sender_id.email)

        # Receiver Data
        submaster_node1 = etree.SubElement(sub_master_node_2,"Destinatario")
        root_node2 = etree.SubElement(submaster_node1,"Identificacion")
        etree.SubElement(root_node2,'Nombre').text = "{}".format(receiver_id.name)
        root_node3 = etree.SubElement(submaster_node1,"DatosDireccion")
        etree.SubElement(root_node3, 'Direccion').text = "{}".format(receiver_id.street)
        etree.SubElement(root_node3, 'Localidad').text = "{}".format(receiver_id.city)
        etree.SubElement(submaster_node1, 'CP').text = "{}".format(receiver_id.zip)
        etree.SubElement(submaster_node1, 'ZIP').text = "{}".format(receiver_id.zip)
        etree.SubElement(submaster_node1, 'Pais').text = "{}".format(receiver_id.country_id and receiver_id.country_id.code)
        etree.SubElement(submaster_node1, 'Telefonocontacto').text = "{}".format(receiver_id.phone)
        etree.SubElement(submaster_node1, "Email").text = "{}".format(receiver_id.email)

        # package Data
        submaster_node2 = etree.SubElement(sub_master_node_2,'Envio')
        etree.SubElement(submaster_node2,'CodProducto').text = "{}".format(self.correos_product_code)
        etree.SubElement(submaster_node2,'TipoFranqueo').text = "{}".format(self.correos_typelock)
        etree.SubElement(submaster_node2,'ModalidadEntrega').text = "{}".format(self.correos_modality_delivery)
        root_node5 =etree.SubElement(submaster_node2,'Pesos')
        sub_root_node = etree.SubElement(root_node5,'Peso')
        etree.SubElement(sub_root_node,'TipoPeso').text = self.correos_weight_type
        etree.SubElement(sub_root_node,'Valor').text = "{0:05.0f}".format(pickings.shipping_weight * 1000)  # we must need to send weight in GRAM.
        etree.SubElement(submaster_node2,'Largo').text = "{}".format(self.correos_packaging_id and self.correos_packaging_id.packaging_length or "")
        etree.SubElement(submaster_node2,'Alto').text = "{}".format(self.correos_packaging_id and self.correos_packaging_id.height or "")
        etree.SubElement(submaster_node2,'Ancho').text = "{}".format(self.correos_packaging_id and self.correos_packaging_id.width or "")
        # INTERNATIONAL DELIVERIES - START - LANDOO
        if sender_id.country_id != receiver_id.country_id:
            root_node6 = etree.SubElement(submaster_node2, 'Aduana')
            etree.SubElement(root_node6, 'TipoEnvio').text = "1"
            root_node7 = etree.SubElement(root_node6, 'DescAduanera')
            root_node8 = etree.SubElement(root_node7, 'DatosAduana')
            etree.SubElement(root_node8, 'Cantidad').text = "1"
            etree.SubElement(root_node8, 'Descripcion').text = "EJEMPLO DE DESCRIPCION DE PRODUCTO"
            etree.SubElement(root_node8, 'Peso').text = "05000"
            etree.SubElement(root_node8, 'Valor').text = "050000"
        # INTERNATIONAL DELIVERIES - END - LANDOO
        return etree.tostring(master_node1)

    @api.model
    def correos_vts_send_shipping(self, pickings):
        if not self.company_id:
            raise ValidationError("Company Is Not Selected In Delivery Method!")
        correos_api_url = self.company_id.correos_api_url
        data = "%s:%s" % (self.company_id.correos_username, self.company_id.correos_password)
        encode_data = base64.b64encode(data.encode("utf-8"))
        authrization_data = "Basic %s" % (encode_data.decode("utf-8"))
        request_data = self.correos_label_request_data(pickings)
        headers = { 'SOAPAction' : 'PreRegistro',
                    'Authorization': authrization_data,
                    'Content-Type': 'text/xml; charset="utf-8"'}
        try:
            _logger.info("POST Request To {}".format(correos_api_url))
            _logger.info("POST Request To {}".format(request_data))
            result = requests.post(url=correos_api_url, data=request_data,headers=headers)
        except Exception as e:
            raise ValidationError(e)
        if result.status_code != 200:
            raise ValidationError(("Label Request Data Invalid! %s ") % (result.content))
        api = correos_response.Response(result)
        result =api.dict()
        _logger.info("Correos Shipment Response Data : %s" % (result))
        result_envelop = result.get('Envelope').get('Body').get('RespuestaPreregistroEnvio')

        binary_data = result_envelop.get('Bulto') and result_envelop.get('Bulto').get('Etiqueta') and result_envelop.get('Bulto').get('Etiqueta').get('Etiqueta_pdf') and result_envelop.get('Bulto').get('Etiqueta').get('Etiqueta_pdf').get('Fichero') or False
        if not binary_data:
            raise ValidationError("Correos Label Not Found In Response %s"%(result_envelop))

        CodExpedicion = result_envelop.get('CodExpedicion')
        tracking_number = result_envelop.get('Bulto').get('CodEnvio')
        CodManifiesto = result_envelop.get('Bulto').get('CodManifiesto')
        binary_data = binascii.a2b_base64(str(binary_data))
        message = (("Label created!<br/> <b>Label Tracking Number : </b>%s<br/> <b> Parcel Number : %s") % (tracking_number,CodExpedicion))
        pickings.message_post(body=message, attachments=[
            ('Label-%s.%s' % (tracking_number, "pdf"), binary_data)])
        pickings.carrier_tracking_ref = tracking_number
        pickings.correos_tracking_id = CodManifiesto
        delivery_price = sum(
            pickings.sale_id and pickings.sale_id.order_line.filtered(lambda line: line.is_delivery).mapped('price_unit'))
        return [{
            'exact_price': delivery_price or 0.0,
            'tracking_number': tracking_number}]


    def correos_vts_cancel_shipment(self, pickings):
        raise ValidationError("Cancel API not provide by Correos")

    def correos_vts_get_tracking_link(self, picking):
        tracking_link = self.company_id.correos_tracking_url if self.company_id and self.company_id.correos_tracking_url else "http://www.correos.es/comun/localizador/track.asp?numero="
        return '{0}{1}'.format(tracking_link, picking.carrier_tracking_ref)
