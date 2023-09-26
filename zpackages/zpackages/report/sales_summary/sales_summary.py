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
#   GROUP BY
#             `tabDelivery Note Item`.item_group, `tabSales Taxes and Charges`.rate
def get_data(filters):
    data = []
    sales_summary = """SELECT
             `tabDelivery Note`.name,
            `tabDelivery Note Item`.item_group,
            `tabDelivery Note Item`.qty AS qty,
            `tabDelivery Note Item`.amount AS amount,
            IFNULL(`tabSales Taxes and Charges`.rate, 0) as rate
        FROM
            `tabDelivery Note`
            LEFT JOIN `tabDelivery Note Item` ON `tabDelivery Note`.name = `tabDelivery Note Item`.parent
            LEFT JOIN `tabSales Taxes and Charges` ON `tabDelivery Note`.name = `tabSales Taxes and Charges`.parent
        WHERE 
            {conditions}
      
    """.format(conditions=get_conditions(filters, "Delivery Note"))

    sales_summary_result = frappe.db.sql(sales_summary, filters, as_dict=1)

    for dt in sales_summary_result:
        tax_rate = dt.get('rate')  if dt.get('rate') else 0  # Assuming rate is the tax rate in percentage
        tax = dt.get('amount') * dt.get('rate') / 100
        dt.update({'total': tax + dt.get('amount'), 'rate': tax_rate, 'tax': tax})

    # grouped_sums = {}
    # for entry in sales_summary_result:
    #     item_group = entry['item_group']
    #     if item_group not in grouped_sums:
    #         grouped_sums[item_group] = {
    #             'item_group': item_group,
    #             'qty': 0,
    #             'amount': 0,
    #             'tax': 0,
    #             'total': 0
    #         }
    #
    #     grouped_sums[item_group]['qty'] += entry['qty']
    #     grouped_sums[item_group]['amount'] += entry['amount']
    #     grouped_sums[item_group]['tax'] += entry['tax']
    #     grouped_sums[item_group]['total'] += entry['total']
    #
    # grouped_sums_list = list(grouped_sums.values())

    data.extend(sales_summary_result)
    return data

