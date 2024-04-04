from odoo import models, fields, api
try:
  import qrcode
except ImportError:
  qrcode = None
try:
  import base64
except ImportError:
  base64 = None
from io import BytesIO

import odoo.exceptions
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta


class Asset(models.Model):
    _name = "asset"

    name = fields.Char(required=1)
    serial = fields.Char()
    price = fields.Float()
    buy_date = fields.Date(default=datetime.now())
    dep_fin_value = fields.Float()
    dep_period = fields.Integer()
    location_id = fields.Many2one("res.company")
    category_id = fields.Many2one("product.category")
    custody_id = fields.Many2one("hr.employee")
    #status = fields.Many2one("status")
    #current_request = fields.Many2many("request")
    sell_price = fields.Float()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('stopped', 'Stopped')
    ], default='active')
    description = fields.Text()
    tag_ids = fields.Many2many('tag')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    current_price = fields.Float(compute='_compute_current_price')
    asset_qr_code = fields.Binary("QR Code", compute='generate_asset_qr_code')

    def generate_asset_qr_code(self):
        for rec in self:
            if qrcode and base64:
                ir_param = self.env['ir.config_parameter'].sudo()
                base_url = ir_param.get_param('web.base.url')
                if base_url:
                    base_url += '/web#&model=%s&id=%s' % (rec._name, rec.id)
                qr = qrcode.QRCode(version=1,
                                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                                   box_size=3,
                                   border=4)
                qr.add_data(base_url)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'asset_qr_code': qr_image})

    @api.onchange('price', 'buy_date', 'dep_period')
    def _compute_current_price(self):
        for rec in self:
            if rec.dep_period > 0:
                rec.current_price = rec.price - ((rec.price / rec.dep_period) * (
                        (datetime.now().year - rec.buy_date.year) * 12
                        + datetime.now().month - rec.buy_date.month))

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_active(self):
        for rec in self:
            rec.state = 'active'

    def action_stop(self):
        for rec in self:
            rec.state = 'stopped'




