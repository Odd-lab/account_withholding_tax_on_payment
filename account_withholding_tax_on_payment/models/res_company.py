from odoo import fields, models
from num2words import num2words


class ResCompany(models.Model):
    _inherit = "res.company"

    wht_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Withholding Tax Sequence",
    )

    def _create_wht_per_company_sequences(self):
        vals_list = []

        for company in self:
            vals_list.append(
                {
                    "name": f"{company.name} - Withholding Tax Sequence",
                    "code": "wht.sequence",
                    "company_id": company.id,
                    "prefix": "WHT/%(range_y)s%(range_month)s",
                    "padding": 4,
                    "implementation": "standard",
                    "number_next": 1,
                    "number_increment": 1,
                    "use_date_range": True,
                }
            )
        if vals_list:
            sequences = self.env["ir.sequence"].create(vals_list)
            for rec in sequences:
                rec.company_id.wht_sequence_id = rec.id

    def th_split_tax_number(self, option="1"):
        return self.partner_id.th_split_tax_number(option)

    def _get_currency_name_hook(self):
        """Hooks to add currency translate.
        Currently, there are 2 currency are USD and EUR"""
        return {"Dollars": "ดอลลาร์", "Euros": "ยูโร", "Cents": "เซนต์"}

    def _convert_currency_name_hook(self, label):
        dict_currency_name = self._get_currency_name_hook()
        return dict_currency_name.get(label, "")

    def amount_to_text(self, amount):
        self.ensure_one()
        lang_code = self.env.context.get("lang") or False
        if lang_code != "th_TH":
            return super().amount_to_text(amount)

        def _num2words(number, lang):
            # lang is 'th' only
            return num2words(number, lang=lang).title()

        integral, _sep, fractional = f"{amount:.{self.decimal_places}f}".partition(
            "."
        )  # noqa: E501
        integer_value = int(integral)
        lang = (
            self.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", lang_code)])
        )
        # Thai Text with Thai Currency
        if self.name == "THB":
            return num2words(amount, to="currency", lang=lang.iso_code)
        # Thai Text with Foreign currency
        currency_unit_label = self._convert_currency_name_hook(self.currency_unit_label)
        amount_words = self.env._(
            "%(integral_amount)s%(currency_unit)s",
            integral_amount=_num2words(integer_value, lang=lang.iso_code),
            currency_unit=currency_unit_label,
        )
        if not self.is_zero(amount - integer_value):
            currency_subunit_label = self._convert_currency_name_hook(
                self.currency_subunit_label
            )
            amount_words += self.env._(
                "%(fractional_amount)s%(currency_subunit)s",
                fractional_amount=_num2words(int(fractional or 0), lang=lang.iso_code),
                currency_subunit=currency_subunit_label,
            )
        return amount_words

    def format_amount(self, value, decimal_places=2, **optional):
        try:
            return "{:,.{}f}".format(float(str(value).replace(",", "")), decimal_places)
        except Exception:
            return value
