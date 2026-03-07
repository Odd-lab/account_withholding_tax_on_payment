from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def th_split_tax_number(self, option="1") -> list | None:
        self.ensure_one()
        if self.vat and len(self.vat) == 13:
            if option == "1":
                card_1 = self.vat[0]
                card_2 = self.vat[1:5]
                card_3 = self.vat[5:10]
                card_4 = self.vat[10:12]
                card_5 = self.vat[12]
                return [card_1, card_2, card_3, card_4, card_5]
            elif option == "2":
                card_1 = self.vat[0]
                card_2 = self.vat[1:5]
                card_3 = self.vat[5:10]
                card_4 = self.vat[10:12]
                card_5 = self.company_id.vat[12]
                return [card_1, card_2, card_3, card_4, card_5]
            if option == "53":
                card_1 = self.vat[0]
                card_2 = self.vat[1:3]
                card_3 = self.vat[3]
                card_4 = self.vat[4:7]
                card_5 = self.vat[7:12]
                card_6 = self.vat[12]
                return [card_1, card_2, card_3, card_4, card_5, card_6]
        return None

    def _get_address_partner(self):
        return ",".join(
            [
                self.env.company.street or "",
                self.env.company.street2 or "",
                self.env.company.state_id.name or "",
                self.env.company.country_id.name or "",
                self.env.company.zip or "",
            ]
        )
