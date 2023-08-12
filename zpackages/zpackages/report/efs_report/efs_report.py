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
            "label": _("Sales Order"),
            "fieldname": "sales_order",
            "fieldtype": "Link",
           "options":'Sales Order'
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Finish Item"),
            "fieldname": "finish_item",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Item Attribute"),
            "fieldname": "item_attribute",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("GSM"),
            "fieldname": "gsm",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": _("Length"),
            "fieldname": "length",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": _("Width"),
            "fieldname": "width",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": _("UPS"),
            "fieldname": "ups",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": _("Color"),
            "fieldname": "color",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": _("As/Size"),
            "fieldname": "as_per_size",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Sheet Qty"),
            "fieldname": "sheet_qty",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Wastage Sheet"),
            "fieldname": "wastage_sheet",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Wastage%"),
            "fieldname": "wastage_percent",
            "fieldtype": "percent",
            "width": 100
        },
        {
            "label": _("Wastage Weight"),
            "fieldname": "wastage_weight",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Weight+Wastage"),
            "fieldname": "weight_with_wastage",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Total Weight+Wastage"),
            "fieldname": "total_wastage_with_weight",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("F.Length"),
            "fieldname": "dni_length",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("F.Width"),
            "fieldname": "dni_width",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("F.Size"),
            "fieldname": "finish_size",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Delivered Qty"),
            "fieldname": "delivered_qty",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Weight Total"),
            "fieldname": "weight_total",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Weight Difference"),
            "fieldname": "weight_diff",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Wastage%"),
            "fieldname": "wastage_percent",
            "fieldtype": "percent",
            "width": 100
        }
    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("customer"):
        conditions.append(f"`tab{doctype}`.customer = %(customer)s")
    if filters.get("sales_order"):
        conditions.append(f"`tab{doctype}`.name = %(sales_order)s")
    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents
    return " AND ".join(conditions)


def get_data(filters):
    data = []
    so_query = """
        SELECT
            `tabSales Order`.name AS sales_order,
            `tabSales Order`.customer,
            `tabSales Order Item`.item_code AS finish_item,
            `tabSales Order Item`.qty,
            `tabRaw Items`.raw_material AS item_attribute,
            `tabRaw Items`.gsm,
            `tabRaw Items`.length,
            `tabRaw Items`.width,
            `tabRaw Items`.ups,
            `tabRaw Items`.color,
            `tabRaw Items`.as_per_size,
            `tabRaw Items`.sheet_qty,
            `tabRaw Items`.color_wastage AS wastage_sheet,
            `tabRaw Items`.color_wastage_percent AS wastage_percent,
            `tabRaw Items`.wastage_weight,
            `tabRaw Items`.weight_with_wastage,
            `tabRaw Items`.final_weight_with_wastage AS total_wastage_with_weight,
            `tabDelivery Note Item`.length AS dni_length,
            `tabDelivery Note Item`.width AS dni_width,
            `tabRaw Items`.as_per_size AS finish_size,
            `tabDelivery Note Item`.qty AS delivered_qty,
            `tabDelivery Note Item`.weight_total,
            (`tabRaw Items`.final_weight_with_wastage - `tabDelivery Note Item`.weight_total) AS weight_diff,
            (`tabRaw Items`.final_weight_with_wastage - `tabDelivery Note Item`.weight_total) / `tabRaw Items`.final_weight_with_wastage AS wastage_percent
        FROM
            `tabSales Order`
        JOIN
            `tabSales Order Item` ON `tabSales Order`.name = `tabSales Order Item`.parent
        JOIN
            `tabRaw Items` ON `tabSales Order`.name = `tabRaw Items`.parent
        JOIN
            `tabDelivery Note Item` ON `tabSales Order`.name = `tabDelivery Note Item`.against_sales_order
        WHERE
            {conditions}
        GROUP BY
                  `tabSales Order Item`.parent
    """.format(conditions=get_conditions(filters, "Sales Order"))

    so_result = frappe.db.sql(so_query, filters, as_dict=1)
    data.extend(so_result)
    return data
