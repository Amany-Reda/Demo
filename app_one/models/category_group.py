from odoo import models, fields


class CategoryGroup(models.Model):
    _name = "category.group"

    name = fields.Char(required=True)
    available = fields.Boolean(default=True)
    category_ids = fields.Many2many('product.category')