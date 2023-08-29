

frappe.query_reports["EFS Report Raw"] = {
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
            "get_query": function () {
                var customer = frappe.query_report.get_filter_value('customer');
                return {
                    filters: {"customer": customer}
                };
            },
        }
    ]
};