from dateutil.relativedelta import relativedelta

from odoo import fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    def _create_date_range_seq(self, date):
        res = super()._create_date_range_seq(date)
        for rec in res:
            dt_from = fields.Date.today()
            new_date_from = dt_from.replace(day=1)
            new_date_to = dt_from + relativedelta(day=31)
            rec.date_from = fields.Date.to_string(new_date_from)
            rec.date_to = fields.Date.to_string(new_date_to)
        return res
