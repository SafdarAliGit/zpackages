import frappe


@frappe.whitelist()
def get_process_wast_percent(**args):
    color = args.get('color')
    if int(color) in (1, 2, 3, 4, 5, 6, 7, 8, 9):
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


@frappe.whitelist()
def get_job_costing_items(**args):
    job_costing = args.get('job_costing')
    parent = frappe.qb.DocType("Job Costing")
    child = frappe.qb.DocType("Job Costing Items")
    query = (
        frappe.qb.from_(parent)
        .from_(child)
        .select(child.raw_material,
                parent.job_costing,
                parent.customer_article_code,
                child.gsm,
                child.width,
                child.length,
                child.ups,
                child.color,
                )
        .where(
            (parent.job_costing == job_costing)
            & (parent.name == child.parent)
            & (parent.docstatus == 1)
        )
    )
    return query.run(as_dict=True)


@frappe.whitelist()
def raw_material_stock_entry(source_name):
    source_name = frappe.get_doc("Sales Order", source_name)
    if not source_name.stock_entry_done:
        try:
            se = frappe.new_doc("Stock Entry")
            se.stock_entry_type = "Material Transfer"
            se.from_warehouse = f"Stores - {get_company_abbr()}"
            se.to_warehouse = f"Work In Progress - {get_company_abbr()}"
            for item in source_name.raw_items:
                it = se.append("items", {})
                it.item_code = item.raw_material
                it.qty = round(item.final_weight_with_wastage)
            se.save()
            source_name.stock_entry_done = 1
            source_name.save()
            return se
        except Exception as error:
            frappe.throw(error)
    else:
        frappe.throw("Raw Stock Entry already created")


def get_company_abbr():
    company_name = frappe.defaults.get_defaults().company
    company = frappe.get_doc('Company', company_name)
    company_abbr = company.get('abbr')
    return company_abbr
