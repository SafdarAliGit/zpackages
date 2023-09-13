from . import __version__ as app_version

app_name = "zpackages"
app_title = "zpackages"
app_publisher = "Tech Ventures"
app_description = "this is printing services application"
app_email = "safdar211@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zpackages/css/zpackages.css"
# app_include_js = "/assets/zpackages/js/zpackages.js"

# include js, css files in header of web template
# web_include_css = "/assets/zpackages/css/zpackages.css"
# web_include_js = "/assets/zpackages/js/zpackages.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "zpackages/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Sales Order": "public/js/sales_order.js", "Stock Entry": "public/js/stock_entry.js","Delivery Note": "public/js/delivery_note.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "zpackages.utils.jinja_methods",
#	"filters": "zpackages.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "zpackages.install.before_install"
# after_install = "zpackages.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "zpackages.uninstall.before_uninstall"
# after_uninstall = "zpackages.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zpackages.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	# "Sales Order": "zpackages.overrides.sales_order_overrides.SalesOrderOverrides",
	"Delivery Note": "zpackages.overrides.delivery_note_overrides.DeliveryNoteOverrides"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"zpackages.tasks.all"
#	],
#	"daily": [
#		"zpackages.tasks.daily"
#	],
#	"hourly": [
#		"zpackages.tasks.hourly"
#	],
#	"weekly": [
#		"zpackages.tasks.weekly"
#	],
#	"monthly": [
#		"zpackages.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "zpackages.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "zpackages.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "zpackages.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["zpackages.utils.before_request"]
# after_request = ["zpackages.utils.after_request"]

# Job Events
# ----------
# before_job = ["zpackages.utils.before_job"]
# after_job = ["zpackages.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"zpackages.auth.validate"
# ]
# required_apps = ["erpnext"]