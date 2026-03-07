{
    "name": "Withholding Tax On Payment",
    "summary": "Create and manage withholding tax documents linked to payments",
    "description": "Manage Withholding Tax (WHT) documents linked to Payments, including certificate report printing and XLSX export.",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "author": "Odd Lab",
    "license": "OPL-1",
    "company": "Odd Lab",
    "website": "https://github.com/tao-thewarat",
    "depends": [
        "l10n_account_withholding_tax",
    ],
    "external_dependencies": {
        "python": [
            "openpyxl",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/paperformat.xml",
        "data/report_data.xml",
        "reports/wht_certificate_report.xml",
        "wizards/account_payment_register_views.xml",
        "views/account_withholding_tax_views.xml",
        "views/res_config_settings_views.xml",
        "views/account_payment_views.xml",
        "views/account_tax_views.xml",
        "views/menuitems.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "account_withholding_tax_on_payment/static/src/css/*.css",
            "account_withholding_tax_on_payment/static/src/css/*.scss",
        ],
    },
    "installable": True,
    "application": False,
    "price": 299.99,
    "currency": "USD",
}
