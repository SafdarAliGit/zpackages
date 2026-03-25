import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Employee",         "fieldname": "employee",          "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name",    "fieldname": "employee_name",     "fieldtype": "Data",  "width": 150},
        {"label": "Branch",           "fieldname": "branch",            "fieldtype": "Data",  "width": 120},
        {"label": "Designation",      "fieldname": "designation",       "fieldtype": "Data",  "width": 130},
        {"label": "Shift",            "fieldname": "shift",             "fieldtype": "Data",  "width": 120},
        {"label": "Shift Start Time", "fieldname": "shift_start_time",  "fieldtype": "Data",  "width": 100},
        {"label": "Shift End Time",   "fieldname": "shift_end_time",    "fieldtype": "Data",  "width": 100},
        {"label": "Check In Time",    "fieldname": "check_in_time",     "fieldtype": "Data",  "width": 110},
        {"label": "Check Out Time",   "fieldname": "check_out_time",    "fieldtype": "Data",  "width": 110},
        {"label": "Working Hours",    "fieldname": "working_hours",     "fieldtype": "Float", "width": 100},
        {"label": "Date",             "fieldname": "attendance_date",   "fieldtype": "Date",  "width": 100},
        {"label": "Status",           "fieldname": "status",            "fieldtype": "Data",  "width": 90},
    ]


def get_data(filters):
    filters = filters or {}

    # Normalize optional params so %(employee)s IS NULL check works in MySQL
    if not filters.get("employee"):
        filters["employee"] = None

    # Build extra conditions for optional filters Branch / Department
    # (appended to the original WHERE clause without modifying it)
    extra = ""
    if filters.get("branch"):
        extra += " AND emp.branch = %(branch)s"
    if filters.get("department"):
        extra += " AND emp.department = %(department)s"

    query = """
        SELECT
            att.employee                                        AS employee,
            att.employee_name                                   AS employee_name,
            emp.branch                                          AS branch,
            emp.designation                                     AS designation,
            att.shift                                           AS shift,
            TIME(st.start_time)                                 AS shift_start_time,
            TIME(st.end_time)                                   AS shift_end_time,
            COALESCE(TIME(att.in_time), '')                     AS check_in_time,
            COALESCE(TIME(att.out_time), '')                    AS check_out_time,
            att.working_hours                                   AS working_hours,
            att.attendance_date                                 AS attendance_date,
            att.status                                          AS status
        FROM `tabAttendance` att
        LEFT JOIN `tabEmployee` emp
            ON emp.name = att.employee
        LEFT JOIN `tabShift Type` st
            ON st.name = att.shift
        WHERE
            att.docstatus = 1
            AND att.attendance_date BETWEEN %(from_date)s AND %(to_date)s
            AND (%(employee)s IS NULL OR %(employee)s = '' OR att.employee = %(employee)s)
            {extra}
        ORDER BY att.attendance_date ASC, att.employee ASC
    """.format(extra=extra)

    return frappe.db.sql(query, filters, as_dict=True)