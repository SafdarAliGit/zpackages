

frappe.query_reports["Sales Summary New"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 1
        },
         {
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
             "options":"Item Group"
        }
    ]
};
