import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
		{
            "label": "Date",
            "fieldname": "attendance_date",
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 120,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Branch",
            "fieldname": "branch",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": "Designation",
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": "Shift",
            "fieldname": "shift",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Shift Start Time",
            "fieldname": "shift_start_time",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": "Shift End Time",
            "fieldname": "shift_end_time",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": "Check In Time",
            "fieldname": "check_in_time",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": "Check Out Time",
            "fieldname": "check_out_time",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": "Working Hours",
            "fieldname": "working_hours",
            "fieldtype": "Float",
            "width": 110,
        },
        
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100,
        },
    ]


def get_data(filters):
    conditions, values = get_conditions(filters)

    query = """
        SELECT
            att.employee,
            att.employee_name,
            emp.branch,
            emp.department,
            emp.designation,
            att.shift,
            TIME(st.start_time)                         AS shift_start_time,
            TIME(st.end_time)                           AS shift_end_time,
            IFNULL(TIME(att.in_time), '')               AS check_in_time,
            IFNULL(TIME(att.out_time), '')              AS check_out_time,
            att.working_hours,
            att.attendance_date,
            att.status
        FROM `tabAttendance` att
        LEFT JOIN `tabEmployee` emp
            ON emp.name = att.employee
        LEFT JOIN `tabShift Type` st
            ON st.name = att.shift
        WHERE
            att.docstatus = 1
            {conditions}
        ORDER BY att.attendance_date ASC, att.employee ASC
    """.format(
        conditions=conditions
    )

    return frappe.db.sql(query, values, as_dict=True)


def get_conditions(filters):
    """
    Build WHERE clause conditions dynamically based on provided filters.
    This avoids passing NULL literals through %(param)s which can behave
    inconsistently across MySQL versions.
    """
    conditions = []
    values = {}

    if not filters:
        return "", values

    # Date range — both are mandatory fields in the report
    if filters.get("from_date"):
        conditions.append("att.attendance_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("att.attendance_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    # Optional filters
    if filters.get("employee"):
        conditions.append("att.employee = %(employee)s")
        values["employee"] = filters["employee"]

    if filters.get("branch"):
        conditions.append("emp.branch = %(branch)s")
        values["branch"] = filters["branch"]

    if filters.get("department"):
        conditions.append("emp.department = %(department)s")
        values["department"] = filters["department"]

    condition_str = ("AND " + " AND ".join(conditions)) if conditions else ""
    return condition_str, values