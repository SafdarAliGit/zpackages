// Copyright (c) 2023, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Costing', {
    // refresh: function(frm) {

    // }
});

frappe.ui.form.on('Job Costing Items', {
    // refresh: function(frm) {

    // }
    ups: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var as_per_size = (((d.gsm * d.width * d.length) / 15500) / 100) / d.ups;
        frappe.model.set_value(cdt, cdn, "as_per_size", as_per_size);
        if (d.finish_qty > 0) {
            var sheet_qty = Math.round(d.finish_qty / d.ups);
            frappe.model.set_value(cdt, cdn, "sheet_qty", sheet_qty);
        } else {
            frappe.throw("Please Set Finish Qty");
        }
    },

    job_costing_items_add: function (frm, cdt, cdn) {
        var qty = frm.doc.qty;
        if (qty) {
            frappe.model.set_value(cdt, cdn, 'finish_qty', qty);
        } else {
            frappe.show_alert("Set Finish Qty");
        }
    },
    color: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        // Ajax call
        frappe.call({
            method: 'zpackages.zpackages.doctype.utils.get_process_wast_percent',
            args: {
                color: d.color,
                sheet_qty: d.sheet_qty,
            },
            callback: function (response) {
                if (response.message) {
                    frappe.model.set_value(cdt, cdn, 'color_wastage_percent', response.message);
                    var color_wastage = d.sheet_qty * (d.color_wastage_percent / 100);
                    frappe.model.set_value(cdt, cdn, 'color_wastage', color_wastage);
                    var wastage_weight = d.as_per_size * (d.color_wastage_percent / 100);
                    frappe.model.set_value(cdt, cdn, 'wastage_weight', wastage_weight);
                    var weight_with_wastage = d.as_per_size + d.wastage_weight;
                    frappe.model.set_value(cdt, cdn, 'weight_with_wastage', weight_with_wastage);
                    var final_weight_with_wastage = parseFloat(d.weight_with_wastage) + parseInt(d.finish_qty);
                    frappe.model.set_value(cdt, cdn, 'final_weight_with_wastage', final_weight_with_wastage);
                    console.log(final_weight_with_wastage);
                }
            }
        });
    }


});
