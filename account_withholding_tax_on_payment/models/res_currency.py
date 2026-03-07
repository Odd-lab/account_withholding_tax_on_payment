from odoo import models
from odoo.tools.float_utils import float_split_str


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def float_split_amount_str(self, amount, precision_digits=False) -> tuple[str]:
        if not precision_digits:
            precision_digits = self.env.company.currency_id.decimal_places

        return float_split_str(amount, precision_digits)
