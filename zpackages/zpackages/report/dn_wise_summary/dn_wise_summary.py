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
            "label": _("Customer PO"),
            "fieldname": "customer_po",
            "fieldtype": "Data",
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
            "label": _("Delivery Location"),
            "fieldname": "delivery_location",
            "fieldtype": "Data",
            "width": 150
        },
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
            "label": _("Contract No"),
            "fieldname": "contract_no",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Article No"),
            "fieldname": "article_no",
            "fieldtype": "Data",
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
            `tabDelivery Note`.name AS id,
            `tabDelivery Note`.naming_series AS id_series,
            `tabDelivery Note`.posting_date AS date, 
            `tabDelivery Note`.customer, 
            `tabDelivery Note Item`.po_no AS customer_po,
            `tabDelivery Note Item`.item_code, 
            `tabDelivery Note Item`.description,
            `tabDelivery Note`.delivery_location,
            `tabDelivery Note Item`.qty,
            `tabDelivery Note Item`.rate,
            `tabDelivery Note Item`.amount,
            (SELECT DISTINCT `rate` FROM `tabSales Taxes and Charges` WHERE `tabDelivery Note`.name = `tabSales Taxes and Charges`.parent) AS rate_of_sales_tax,
            `tabDelivery Note Item`.contract_no,
            `tabDelivery Note Item`.contract_no,
            `tabDelivery Note Item`.article_no,
            `tabDelivery Note Item`.item_group,
            `tabDelivery Note`.status
        FROM
            `tabDelivery Note`
        LEFT JOIN
            `tabDelivery Note Item` ON `tabDelivery Note`.name = `tabDelivery Note Item`.parent
        LEFT JOIN 
            `tabSales Taxes and Charges` ON `tabDelivery Note Item`.name = `tabSales Taxes and Charges`.parent AND `tabDelivery Note Item`.idx = `tabSales Taxes and Charges`.idx
        WHERE 
            {conditions}
        ORDER BY 
            `tabDelivery Note`.modified DESC
    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)

    data.extend(sales_summary_result)
    return data

