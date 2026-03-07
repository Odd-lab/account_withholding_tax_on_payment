from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_open_withholding_tax(self):
        self.ensure_one()
        withholding = self.env["account.withholding.tax"].search(
            [("payment_id", "=", self.id)]
        )
        return withholding._get_records_action(name=self.env._("Withholding Tax"))
