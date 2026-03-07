from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    wht_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Withholding Tax Sequence",
        related="company_id.wht_sequence_id",
        readonly=False,
    )
