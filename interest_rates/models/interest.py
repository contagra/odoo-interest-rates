import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class Interest(models.Model):
    _name = "interest"
    _description = "Interest"
    _order = 'active desc, name'

    name = fields.Char(string='Name', required=True)
    rate = fields.Float(compute='_compute_current_rate', string='Current Rate', digits=0,
                        help='The rate current interest rate')
    rate_ids = fields.One2many('interest.rate', 'interest_id', string='Rates')
    active = fields.Boolean(default=True)
    date = fields.Date(compute='_compute_date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_name', 'unique (name,company_id)', 'The interest name must be unique!'),
    ]

    def _get_rates(self, date):
        self.env['interest.rate'].flush(['rate', 'interest_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate FROM interest_rate r
                                  WHERE r.interest_id = c.id AND r.name <= %s
                               ORDER BY r.name DESC
                                  LIMIT 1), 0.0) AS rate
                   FROM interest c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, tuple(self.ids)))
        interest_rates = dict(self._cr.fetchall())
        return interest_rates

    @api.depends('rate_ids.rate')
    def _compute_current_rate(self):
        date = self._context.get('date') or fields.Date.today()
        # selects the last rate before date
        interest_rates = self._get_rates(date)
        for interest in self:
            interest.rate = interest_rates.get(interest.id) or 0.0

    @api.depends('rate_ids.name')
    def _compute_date(self):
        for interest in self:
            interest.date = interest.rate_ids[:1].name
