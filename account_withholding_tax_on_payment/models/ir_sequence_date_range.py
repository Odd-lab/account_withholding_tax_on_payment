from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class IrSequenceDateRange(models.Model):
    _inherit = "ir.sequence.date_range"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            dt_from = fields.Date.today()
            new_date_from = dt_from.replace(day=1)
            new_date_to = dt_from + relativedelta(day=31)
            vals["date_from"] = fields.Date.to_string(new_date_from)
            vals["date_to"] = fields.Date.to_string(new_date_to)
        return super().create(vals_list)
