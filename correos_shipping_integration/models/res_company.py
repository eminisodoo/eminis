from odoo import models, fields, api


class CorreosResCompany(models.Model):
    _inherit = 'res.company'

    correos_username = fields.Char(string="Username", help="Your Correos Account Username")
    correos_password = fields.Char(string="Password", help="Your Correos Account Password")
    correos_customer_code = fields.Char(string="Customer Code", help="Your Correos Account Customer Code")
    correos_api_url = fields.Char(string="API URl")
    correos_tracking_url = fields.Char(string="Tracking URL", help="Used For Tracking Shipment")
    use_correos_shipping_provider = fields.Boolean(copy=False, string="Are You Using Correos?",
                                                 help="If use Correos shipping Integration then set value to TRUE.",
                                                 default=False)
