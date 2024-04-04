from odoo import models, fields
from datetime import datetime


class MakeOrder(models.Model):
    _name = "make.order"

    custody_id = fields.Many2one('hr.employee')
    category_group_ids = fields.Many2one('category.group')

    order_date = fields.Date(default=datetime.now())

    start_date = fields.Date()
    end_date = fields.Date()

    act_start_date = fields.Date()
    act_end_date = fields.Date()

    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('running', 'Running'),
    ], default='pending')
    tag_ids = fields.Many2many('tag')
    description = fields.Text()
