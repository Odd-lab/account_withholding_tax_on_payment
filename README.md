# Account Withholding Tax On Payment

This addon for managing **Withholding Tax (WHT)** documents linked to **Payments**, with support for printing/exporting **withholding tax certificates** based on the format used in the system.

## Key Features

- Adds a dedicated **Withholding Tax** menu and document model (`account.withholding.tax`)
- Links Withholding Tax documents with `account.payment`
- Adds a button on the Payment form to open the related Withholding Tax document
- Supports **WHT Payment** options:
  - `(1) Withheld at source`
  - `(2) Issued for life`
  - `(3) One-time issuance`
  - `(4) Others`
- Adds **Tax Section** field on WHT lines in:
  - Payment Register Wizard (`account.payment.register`)
  - Payment Form (`account.payment`)
  - Withholding Tax Form (`account.withholding.tax`)
- Requires the **Other** field when `tax_section` is `425` or `6`
- Generates WHT document numbers using a company-specific sequence
- On confirmation, validates that the related Payment is in **paid** state
- Exports documents to **XLSX** using a template (`static/template/withholding_tax_template.xlsx`)
- Provides a QWeb report / printable withholding tax certificate

## Dependencies

This module depends on the following modules:

- `l10n_account_withholding_tax`

## Installation

- Place this addon in the Odoo addons path
- Update the app list and install the module: `Account Withholding Tax On Payment`

## Configuration

### 1) Withholding Tax Sequence (Per Company)

Go to:

- **Settings**
- **Accounting** (Tax configuration section)
- **Withholding Tax Sequence**

This field is linked to `res.company.wht_sequence_id`.

Notes:

- If no sequence is configured, the system will automatically create one when confirming a Withholding Tax document
- Default prefix: `WHT/%(range_y)s%(range_month)s`

## Usage

### A) Create WHT from Payment Register (Recommended)

1. Open a Vendor Bill / Invoice and click **Register Payment**
2. Open the **Withholding Tax** tab in the wizard
3. Fill in the withholding lines and select the correct `tax_section`
4. Select **WHT Payment** (shown when withholding tax is applied)
5. Confirm the payment

The system will:

- Create an `account.payment`
- Automatically create an `account.withholding.tax` document (if withholding lines exist)
- Assign sequence numbers (`name`) to WHT lines from the related `account.tax.withholding_sequence_id`

### B) Open Withholding Tax from Payment

On the Payment form, a **Withholding Tax** stat button will appear when `withholding_line_ids` exist.  
This button opens the Withholding Tax document linked to that payment.

### C) Confirm / Set to Draft

On the Withholding Tax document:

- **Confirm**: changes the state to `done`
  - Only available when the document is in `draft`
  - Only allowed when `payment_id.state == 'paid'`
  - Generates the document number (`name`) from the sequence if the current value is `/`
  - Generates `pnd_sequence` based on `pnd_type` if it is not yet assigned
- **Set to Draft**: resets the document back to `draft`

### D) Export XLSX

Click **Export XLSX** on the Withholding Tax document.

- The system fills data into the XLSX template and returns the file for download
- Supports signature stamping based on `is_stamp_signature` and the creator’s signature information

## Notes / Constraints

- Withholding Tax documents in `done` state **cannot be deleted**
- `pnd_type` is computed from tags on `account.tax` invoice repartition lines (such as `+PND3`, `+PND53`, `-PND3`, `-PND53`)
- Reports and XLSX exports use Thai formatting (`th_TH`) and support Buddhist Era (B.E.) year formatting in some date fields

## Technical Overview

- Main model: `account.withholding.tax`
- Line model: `account.withholding.tax.line` (inherits `account.withholding.line`)
- Integrations:
  - wizard: `account.payment.register` creates WHT after payment creation
  - payment: adds method `action_open_withholding_tax`
  - settings: adds `wht_sequence_id` field in `res.config.settings`

## Maintainer

- **Odd Lab**
