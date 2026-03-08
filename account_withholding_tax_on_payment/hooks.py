def pre_init_hook(env):
    lang_th = env.ref("base.lang_th", raise_if_not_found=False)
    if lang_th and not lang_th.active:
        lang_th.write({"active": True})

    taxes = env["account.tax"].search([("is_withholding_tax_on_payment", "=", True)])
    taxes._onchange_is_withholding_tax_on_payment()
