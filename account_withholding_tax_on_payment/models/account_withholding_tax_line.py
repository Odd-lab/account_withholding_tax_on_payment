from odoo import api, fields, models


class AccountWithholdingTaxLine(models.Model):
    _name = "account.withholding.tax.line"
    _inherit = "account.withholding.line"
    _description = "Account Withholding Tax Line"
    _check_company_auto = True

    withholding_tax_id = fields.Many2one(
        comodel_name="account.withholding.tax",
        required=True,
        ondelete="cascade",
    )

    @api.depends("withholding_tax_id.company_id")
    def _compute_company_id(self):
        for rec in self:
            rec.company_id = rec.withholding_tax_id.company_id

    @api.depends("withholding_tax_id.document_date")
    def _compute_comodel_date(self):
        for rec in self:
            rec.comodel_date = rec.withholding_tax_id.document_date

    @api.depends("withholding_tax_id.wht_payment")
    def _compute_comodel_payment_type(self):
        for rec in self:
            rec.comodel_payment_type = rec.withholding_tax_id.payment_id.payment_type

    @api.depends("withholding_tax_id.company_id.currency_id")
    def _compute_comodel_currency_id(self):
        for rec in self:
            rec.comodel_currency_id = rec.withholding_tax_id.company_id.currency_id

    @api.depends("withholding_tax_id.payment_id.payment_type")
    def _compute_type_tax_use(self):
        for rec in self:
            rec.type_tax_use = (
                "purchase"
                if rec.withholding_tax_id.payment_id.payment_type == "outbound"
                else "sale"
            )

    def _get_comodel_partner(self):
        self.ensure_one()
        return self.withholding_tax_id.partner_id or self.env["res.partner"]

    def _get_valid_liquidity_accounts(self):
        self.ensure_one()
        pay = self.withholding_tax_id.payment_id
        return pay._get_valid_liquidity_accounts() if pay else ()
