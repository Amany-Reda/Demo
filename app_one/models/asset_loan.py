from odoo import models, fields, api
from datetime import datetime, timedelta


class AssetLoan(models.Model):
    _name = "asset.loan"

    asset_id = fields.Many2many('asset')
    start_date = fields.Date(default=datetime.now())
    end_date = fields.Date()
    location_id = fields.Many2one("res.company")
    custody = fields.Many2one("hr.employee")

    loan_accepted = fields.Date()
    loan_started = fields.Date()
    loan_returned = fields.Date()

    state = fields.Selection([('pending', 'Pending'),
                              ('accepted', 'Accepted'),
                              ('running', 'Running'),
                              ('rejected', 'Rejected'),
                              ('expired', 'Expired'),
                              ('returned', 'Returned')])

    def action_pending(self):
        self.loan_accepted = None
        self.loan_returned = None
        self.loan_started = None
        self.state = 'pending'

    def action_accept(self):
        self.loan_accepted = datetime.now()
        self.state = 'accepted'

    def action_reject(self):
        self.state = 'rejected'

    def action_expire(self):
        self.state = 'expired'

    def action_return(self):
        self.loan_returned = datetime.now()
        self.state = 'returned'

    def action_running(self):
        self.loan_started = datetime.now()
        self.state = 'running'


    def action_asset(self):
        ctx = {'default_custody_id': self.custody.id,

               }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'asset',
            'view_id': self.env.ref('app_one.asset_view_form').id,
            'res_id': self.asset_id.id ,
            'context': ctx,
        }
