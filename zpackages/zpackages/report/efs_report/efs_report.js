
frappe.query_reports["EFS Report"] = {
    "filters": [

        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
        },
        {
            "fieldname": "sales_order",
            "label": __("Sales Order"),
            "fieldtype": "Link",
            "options": 'Sales Order'
        }
    ],

};
