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
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": 'Item'
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
    conditions.append(f"`tab{doctype}`.docstatus <= 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    sales_summary = """SELECT
            `tabDelivery Note Item`.item_code,
            SUM(`tabDelivery Note Item`.qty) AS qty,
            SUM(`tabDelivery Note Item`.amount) AS amount
        FROM
            `tabDelivery Note`, `tabDelivery Note Item`
        WHERE 
            `tabDelivery Note`.name = `tabDelivery Note Item`.parent AND
            {conditions}
        GROUP BY
            `tabDelivery Note Item`.item_code
    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)
    data.extend(sales_summary_result)
    return data
