// Client-side filters and column formatters
// for Employee Attendance Report

frappe.query_reports["Employee Attendance"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.month_start(),
            reqd: 1,
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.month_end(),
            reqd: 1,
        },
        {
            fieldname: "employee",
            label: __("Employee"),
            fieldtype: "Link",
            options: "Employee",
            reqd: 0,
        },
        {
            fieldname: "branch",
            label: __("Branch"),
            fieldtype: "Link",
            options: "Branch",
            reqd: 0,
        },
        {
            fieldname: "department",
            label: __("Department"),
            fieldtype: "Link",
            options: "Department",
            reqd: 0,
        },
    ],

    formatter: function (value, row, column, data, default_formatter) {
        // Apply default formatting first
        value = default_formatter(value, row, column, data);

        // Colour-code the Status column
        if (column.fieldname === "status" && data) {
            if (data.status === "Present") {
                value = `<span style="color: #2ecc71; font-weight: bold;">${data.status}</span>`;
            } else if (data.status === "Absent") {
                value = `<span style="color: #e74c3c; font-weight: bold;">${data.status}</span>`;
            } else if (data.status === "Half Day") {
                value = `<span style="color: #f39c12; font-weight: bold;">${data.status}</span>`;
            } else if (data.status === "On Leave") {
                value = `<span style="color: #3498db; font-weight: bold;">${data.status}</span>`;
            } else if (data.status === "Work From Home") {
                value = `<span style="color: #9b59b6; font-weight: bold;">${data.status}</span>`;
            }
        }

        // Show check-in time in green if present, red dash if missing
        if (column.fieldname === "check_in_time" && data) {
            if (data.check_in_time) {
                value = `<span style="color: #2ecc71;">✓ ${data.check_in_time}</span>`;
            } else {
                value = `<span style="color: #e74c3c;">✗</span>`;
            }
        }

        // Show check-out time in green if present, red dash if missing
        if (column.fieldname === "check_out_time" && data) {
            if (data.check_out_time) {
                value = `<span style="color: #2ecc71;">✓ ${data.check_out_time}</span>`;
            } else {
                value = `<span style="color: #e74c3c;">✗</span>`;
            }
        }

        // Highlight low working hours in orange
        if (column.fieldname === "working_hours" && data) {
            const hours = parseFloat(data.working_hours) || 0;
            if (hours > 0 && hours < 4) {
                value = `<span style="color: #f39c12; font-weight: bold;">${hours.toFixed(2)}</span>`;
            } else if (hours >= 4) {
                value = `<span style="color: #2ecc71;">${hours.toFixed(2)}</span>`;
            }
        }

        return value;
    },
};