# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        filters = {}
    data = []
    columns = get_columns()
    data = get_data(filters)
    print(data)
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
        }
    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("customer"):
        conditions.append(f"`tab{doctype}`.customer = %(customer)s")
    if filters.get("sales_order"):
        conditions.append(f"`tab{doctype}`.name = %(sales_order)s")
    # conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    so_query = """SELECT
                        so.name AS sales_order,
                        so.customer,
                        soi.item_code as finish_item,
                        soi.qty,
                        ri.raw_material as item_attribute,
                        ri.gsm,
                        ri.length,
                        ri.width,
                        ri.ups,
                        ri.color,
                        ri.as_per_size,
                        ri.sheet_qty,
                        ri.color_wastage as wastage_sheet,
                        ri.color_wastage_percent as wastage_percent,
                        ri.wastage_weight,
                        ri.weight_with_wastage,
                        ri.final_weight_with_wastage as total_wastage_with_weight,
                        dni.length as dni_length,
                        dni.width as dni_width,
                        ri.as_per_size as finish_size,
                        dni.qty as delivered_qty,
                        dni.weight_total                      
                    FROM
                        `tabSales Order` so
                    JOIN
                        `tabSales Order Item` soi ON so.name = soi.parent
                    JOIN
                        `tabRaw Items` ri ON so.name = ri.parent
                    JOIN
                        `tabDelivery Note Item` dni ON so.name = dni.against_sales_order
           
                        """.format(conditions=get_conditions(filters, "Sales Order"))

    so_result = frappe.db.sql(so_query, filters, as_dict=1)
    data.extend(so_result)
    return data
