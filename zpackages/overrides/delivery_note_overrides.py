import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote


class DeliveryNoteOverrides(DeliveryNote):
    def before_submit(self):
        source_name = frappe.get_doc("Delivery Note", self.name)
        try:
            si = frappe.new_doc("Sales Invoice")
            si.posting_date = source_name.posting_date
            si.customer = source_name.customer
            si.delivery_note_id = source_name.name
            si.company = frappe.defaults.get_defaults().company
            si.taxes_and_charges = source_name.taxes_and_charges if source_name.taxes_and_charges else "Pakistan Tax"
            si.update_stock = 1

            for item in source_name.items:
                sii = si.append("items", {})
                sii.item_code = item.item_code
                sii.qty = item.qty
                sii.rate = item.rate
                sii.amount = item.amount
                sii.uom = frappe.defaults.get_defaults().uom
                sii.stock_qty = item.qty
                sii.base_rate = item.rate
                sii.base_amount = item.amount
                sii.allow_zero_valuation_rate = 1
                sii.job_costing = item.job_costing
                sii.length = item.length
                sii.width = item.width
                sii.weight_per_piece = item.weight_per_piece
                sii.gsm = item.gsm
                sii.weight_total = item.weight_total
                sii.weight_with_wastage = item.weight_with_wastage
                sii.weight_total_raw = item.weight_total_raw

            for tax in source_name.taxes:
                tii = si.append("taxes", {})
                tii.account_head = tax.account_head
                tii.rate = tax.rate
                tii.tax_amount = tax.tax_amount
                tii.base_tax_amount = tax.base_tax_amount
                tii.total = tax.total
                tii.base_total = tax.base_total
                tii.description = tax.description
                tii.charge_type = tax.charge_type
                tii.cost_center = tax.cost_center
                tii.tax_amount_after_discount_amount = tax.tax_amount_after_discount_amount
            si.save()
        except Exception as error:
            frappe.throw(f"{error}")