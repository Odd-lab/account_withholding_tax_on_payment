from odoo import Command, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    wht_payment = fields.Selection(
        selection=lambda self: self.env["account.withholding.tax"]._get_wht_payment(),
        default="wht",
        string="WHT Payment",
        required=True,
    )

    def _create_payment_vals_from_wizard(self, batch_result) -> dict:
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        if "withholding_line_ids" in payment_vals:
            payment_vals["withholding_line_ids"] = [
                Command.create(
                    {
                        **vals,
                        "tax_section": wizard.tax_section,
                    }
                )
                for wizard, (_, _, vals) in zip(
                    self.withholding_line_ids,
                    payment_vals["withholding_line_ids"],
                    strict=False,
                )
            ]
        return {
            **payment_vals,
        }

    def _create_payments(self) -> models.Model:
        res = super()._create_payments()
        if self.withholding_line_ids:
            self._create_withholding_tax(payment=res)
        return res

    def _create_withholding_tax(self, payment: models.Model) -> models.Model:
        wht = self.env["account.withholding.tax"].create(
            {
                "wht_payment": self.wht_payment,
                "partner_id": payment.partner_id.id,
                "payment_id": payment.id,
                "document_date": payment.date,
                "source_document": payment.invoice_ids.name,
                "move_ids": payment.invoice_ids.ids,
                "withholding_line_ids": self._prepare_withholding_lines(),
            }
        )
        self._assign_withholding_sequence(wht=wht)
        return wht

    def _prepare_withholding_lines(self) -> list:
        return [
            Command.create(
                {
                    **{
                        k: v
                        for k, v in vals.items()
                        if k not in ("payment_register_id", "placeholder_value")
                    },
                    "tax_section": wizard.tax_section,
                }
            )
            for wizard, vals in zip(
                self.withholding_line_ids.with_context(active_test=False),
                self.withholding_line_ids.with_context(active_test=False).copy_data(),
                strict=False,
            )
        ]

    def _assign_withholding_sequence(self, wht: models.Model):
        for rec in wht.withholding_line_ids:
            rec.name = rec.tax_id.withholding_sequence_id.next_by_id()
