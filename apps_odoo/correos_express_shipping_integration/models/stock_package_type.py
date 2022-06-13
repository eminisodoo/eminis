from odoo import fields, models

class PackageType(models.Model):
    _inherit = 'stock.package.type'
    package_carrier_type = fields.Selection(selection_add=[("correos_express","Correos Express")])
