// Copyright (c) 2023, Tech Ventures and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Summary Eval"] = {
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
