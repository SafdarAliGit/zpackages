import frappe


@frappe.whitelist()
def get_process_wast_percent(**args):
    color = args.get('color')
    if int(color) in (1,2,3,4,5,6,7,8,9):
        selected_color = color
    else:
        frappe.throw("Invalid color selection")
    sheet_qty = int(args.get('sheet_qty'))
    if sheet_qty >= 1000:
        sq = 1000
    elif sheet_qty >= 500 and sheet_qty < 1000:
        sq = 500
    elif sheet_qty >= 250 and sheet_qty < 500:
        sq = 250
    elif sheet_qty >= 150 and sheet_qty < 250:
        sq = 150
    else:
        frappe.throw("Invalid Sheet Qty")
    pwi = frappe.qb.DocType("Process Wastage items")
    query = (
        frappe.qb.from_(pwi)
        .select(pwi.wastage_percent,
                )
        .where(
            (pwi.no_of_color == selected_color)
            & (pwi.sheet_qty == sq)
        )
    )
    return query.run(as_dict=True)[0].wastage_percent