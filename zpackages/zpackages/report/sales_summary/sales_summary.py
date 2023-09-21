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
            "options": 'Item',
            "width": 150
        }
        , {
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
        ,
        {
            "label": _("Tax Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Tax"),
            "fieldname": "tax",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Grand Total"),
            "fieldname": "total",
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


# SUM(`tabDelivery
# Note
# `.total_taxes_and_charges) AS
# taxes,
#
# GROUP BY
#             `tabDelivery Note Item`.item_group
def get_data(filters):
    data = []
    sales_summary = """SELECT
             `tabDelivery Note`.name,
            `tabDelivery Note Item`.item_group,
            SUM(`tabDelivery Note Item`.qty) AS qty,
            SUM(`tabDelivery Note Item`.amount) AS amount
        FROM
            `tabDelivery Note`, `tabDelivery Note Item` 
        WHERE 
            `tabDelivery Note`.name = `tabDelivery Note Item`.parent AND
            {conditions}
        GROUP BY
            `tabDelivery Note Item`.item_group

    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)

    for dt in sales_summary_result:
        stc = frappe.get_all('Sales Taxes and Charges', filters={'parent': dt.get('name')}, fields=['rate'])
        tax_rate = stc[0].get('rate') if stc else 0  # Assuming rate is the tax rate
        tax = dt.get('amount') * tax_rate/100
        dt.update({'rate':tax_rate, 'tax': tax})
        dt.update({'total': tax + dt.get('amount')})

    # for dt in sales_summary_result:
    #     dt.update({'amount':dt.get('total') - dt.get('taxes')})
    data.extend(sales_summary_result)
    return data
