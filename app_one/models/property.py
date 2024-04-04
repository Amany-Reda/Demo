import odoo.exceptions
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=1)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Datetime(default=datetime.now())
    date_availability2 = fields.Datetime(default=datetime.now() + timedelta(hours=6))
    expected_price = fields.Float()
    selling_price = fields.Float()
    profit = fields.Float(compute='_compute_profit')
    living_area = fields.Integer(default=1)
    bedrooms = fields.Integer(required=1)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West '),
    ], default="north")
    owner_id = fields.Many2one('owner')
    sale_order_id = fields.Many2one('sale.order')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
        ], default="draft"
    )
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is already exist!')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Bedrooms must be greater than 0')

    def _create(self, data_list):
        res = super(Property, self)._create(data_list)
        print('Create')
        return res

    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print('Search')
        return res

    def _write(self, vals):
        res = super(Property, self)._write(vals)
        print('Update')
        return res

    def unlink(self):
        res = super(Property, self).unlink()
        print('Delete')
        return res

    def action_draft(self):
        for rec in self:
            rec.state == 'draft'

    def action_pending(self):
        for rec in self:
            rec.state == 'pending'

    def action_sold(self):
        for rec in self:
            rec.state == 'sold'

    @api.depends('expected_price', 'selling_price')
    def _compute_profit(self):
        for rec in self:
            rec.profit = rec.expected_price - rec.selling_price

    @api.onchange('expected_price', 'selling_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.profit < 0:
                raise odoo.exceptions.ValidationError('خسرانه يا صاحبي')
