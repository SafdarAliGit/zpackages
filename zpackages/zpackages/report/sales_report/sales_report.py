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
            "label": _("Id"),
            "fieldname": "id",
            "fieldtype": "Link",
            "options": 'Delivery Note',
            "width": 150
        },{
            "label": _("Id Series"),
            "fieldname": "id_series",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": 'Customer',
            "width": 150
        },


        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": 'Item',
            "width": 150
        } ,

        {
            "label": _("Description"),
            "fieldname": "description",
            "fieldtype": "Data",
            "width": 150
        } ,

        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 150
        }
        ,
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 150
        },

    {
        "label": _("Rate of Sales Tax"),
        "fieldname": "rate_of_sales_tax",
        "fieldtype": "Currency",
        "width": 150
    },


        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
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
            `tabSales Invoice`.name AS id,
            `tabSales Invoice`.naming_series AS id_series,
            `tabSales Invoice`.posting_date AS date, 
            `tabSales Invoice`.customer, 
            `tabSales Invoice Item`.item_code, 
            `tabSales Invoice Item`.description,
            `tabSales Invoice Item`.qty,
            `tabSales Invoice Item`.rate,
            `tabSales Invoice Item`.amount,
            (SELECT DISTINCT `rate` FROM `tabSales Taxes and Charges` WHERE `tabSales Invoice`.name = `tabSales Taxes and Charges`.parent) AS rate_of_sales_tax,
            `tabSales Invoice Item`.item_group,
            `tabSales Invoice`.status
        FROM
            `tabSales Invoice`
        LEFT JOIN
            `tabSales Invoice Item` ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
        LEFT JOIN 
            `tabSales Taxes and Charges` ON `tabSales Invoice Item`.name = `tabSales Taxes and Charges`.parent AND `tabSales Invoice Item`.idx = `tabSales Taxes and Charges`.idx
        WHERE 
            {conditions} AND
            `tabSales Invoice`.docstatus <= 1
        ORDER BY 
            `tabSales Invoice`.modified DESC
    """.format(conditions=get_conditions(filters, "Sales Invoice"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)

    data.extend(sales_summary_result)
    return data

