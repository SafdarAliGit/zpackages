import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder


class SalesOrderOverrides(SalesOrder):
    def on_submit(self):
        pass


@frappe.whitelist()
def raw_material_stock_entry(source_name):
    source_name = frappe.get_doc("Sales Order", source_name)
    if not source_name.stock_entry_done:
        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Material Transfer"
            se.from_warehouse = "Stores - Z"
            se.to_warehouse = "Work In Progress - Z"
            for item in source_name.raw_items:
                it = se.append("items", {})
                it.item_code = item.raw_material
                it.qty = round(item.final_weight_with_wastage)
            se.save()
            source_name.stock_entry_done = 1
            source_name.save()
            return se
        except Exception as error:
            frappe.throw(error)
    else:
        frappe.throw("Raw Stock Entry already created")
