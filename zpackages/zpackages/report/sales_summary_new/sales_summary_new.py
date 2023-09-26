# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": 'Item Group',
            "width": 150
        },

        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 150
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")
    if filters.get("item_group"):
        conditions.append(f"`tab{doctype} Item`.item_group = %(item_group)s")

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    sales_summary = """SELECT 
            SUM(`tabDelivery Note Item`.amount) AS amount, 
            `tabDelivery Note Item`.item_group,
            SUM(`tabDelivery Note Item`.qty) AS qty
        FROM
            `tabDelivery Note`
        LEFT JOIN
            `tabDelivery Note Item` ON `tabDelivery Note`.name = `tabDelivery Note Item`.parent
        WHERE 
            `tabDelivery Note`.status != 'Cancelled' AND
            {conditions}
        GROUP BY
            `tabDelivery Note Item`.item_group
        ORDER BY `tabDelivery Note`.modified DESC
    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)
    data.extend(sales_summary_result)
    return data
