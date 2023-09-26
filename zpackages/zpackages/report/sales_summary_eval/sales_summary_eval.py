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
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": 'Item',
            "width": 150
        },{
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": 'Item Group',
            "width": 150
        },
        {
            "label": _("Voucher #"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": 'Delivery Note',
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150
        }
        ,
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        }
        ,

        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 150
        }
        ,

        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 150
        } ,

        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 150
        }
        ,
        {
            "label": _("Grand Total"),
            "fieldname": "base_grand_total",
            "fieldtype": "Currency",
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
    sales_summary = """SELECT `tabDelivery Note`.name,
            `tabDelivery Note`.customer, 
            `tabDelivery Note`.posting_date, 
            `tabDelivery Note`.status,
            `tabDelivery Note`.customer_name,
            `tabDelivery Note`.base_grand_total,
            `tabDelivery Note Item`.amount, 
            `tabDelivery Note Item`.item_group,
            `tabDelivery Note Item`.item_code,
            `tabDelivery Note Item`.qty,
            `tabDelivery Note Item`.rate
        FROM
            `tabDelivery Note`
        LEFT JOIN
            `tabDelivery Note Item` ON `tabDelivery Note`.name = `tabDelivery Note Item`.parent
        WHERE 
            `tabDelivery Note`.status != 'Cancelled' AND
            {conditions}
        ORDER BY `tabDelivery Note`.modified DESC
    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)
    data.extend(sales_summary_result)
    return data

