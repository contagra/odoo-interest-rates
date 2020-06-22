import logging
from odoo import api, fields, models, _
import time

_logger = logging.getLogger(__name__)

class InterestRate(models.Model):
    _name = "interest.rate"
    _description = "Interest Rate"
    _order = "name desc"

    name = fields.Date(string='Date', required=True, index=True,
                           default=lambda self: fields.Date.today())
    rate = fields.Float(digits=0, default=0.0, help='The rate of interest')
    interest_id = fields.Many2one('interest', string='Interest', readonly=True)

    _sql_constraints = [
        ('unique_name_per_day', 'unique (name,interest_id)', 'Only one interest rate per day allowed!'),
    ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator in ['=', '!=']:
            try:
                date_format = '%Y-%m-%d'
                if self._context.get('lang'):
                    lang_id = self.env['res.lang']._search([('code', '=', self._context['lang'])], access_rights_uid=name_get_uid)
                    if lang_id:
                        date_format = self.browse(lang_id).date_format
                name = time.strftime('%Y-%m-%d', time.strptime(name, date_format))
            except ValueError:
                try:
                    args.append(('rate', operator, float(name)))
                except ValueError:
                    return []
                name = ''
                operator = 'ilike'
        return super(InterestRate, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
