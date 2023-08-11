frappe.query_reports["EFS Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 1  // Set the "reqd" attribute to make the filter mandatory
        },
        {
            "fieldname": "sales_order",
            "label": __("Sales Order"),
            "fieldtype": "Link",
            "options": 'Sales Order',
            "reqd": 1  // Set the "reqd" attribute to make the filter mandatory
        }
    ]
};
