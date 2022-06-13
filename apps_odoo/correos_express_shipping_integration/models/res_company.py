# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CorreosExpressResCompany(models.Model):
    _inherit = 'res.company'

    correos_express_username = fields.Char(string="Correos Express Username", help="Your Correos Account Username")
    correos_express_password = fields.Char(string="Correos Express Password", help="Your Correos Account Password")
    correos_express_customer_code = fields.Char(string="Correos Express Customer Code", help="Your Correos Account Customer Code")
    correso_express_sender_code = fields.Char(string="Correos Express Sender Code",help="Sender's Code ( provided by Correos Express)")
    correos_express_api_url = fields.Char(string="Correos API URl")
    use_correos_express_shipping_provider = fields.Boolean(copy=False, string="Are You Using Correos Express?",
                                                 help="If use Correos Express shipping Integration than value set TRUE.",
                                                 default=False)
