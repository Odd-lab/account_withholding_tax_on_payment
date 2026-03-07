from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.onchange("is_withholding_tax_on_payment")
    def _onchange_is_withholding_tax_on_payment(self):
        if self.is_withholding_tax_on_payment and not self.withholding_sequence_id:
            self.withholding_sequence_id = self.env.ref(
                "account_withholding_tax_on_payment.account_wht_sequence"
            )
