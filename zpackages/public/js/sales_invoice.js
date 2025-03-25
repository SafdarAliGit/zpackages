frappe.ui.form.on("Sales Invoice", {

    refresh: function(frm) {
        // set_weight(frm);
    },
    work_type: function (frm) {
        set_weight(frm);
    },
});

frappe.ui.form.on("Sales Invoice Item", {
    qty: function (frm, cdt, cdn) {
        if (flt(frm.doc.avg_rate) > 0) {
            var row = locals[cdt][cdn];
            frappe.model.set_value(cdt, cdn, "weight", (row.amount * (flt(frm.doc.percentage) / 100))/flt(frm.doc.avg_rate));
        }
        set_total_weight(frm);
    }
});

function set_weight(frm) {
 
    frm.doc.items.forEach(d => {
         if (flt(frm.doc.avg_rate) > 0) {
             frappe.model.set_value(d.doctype, d.name, "weight", (d.amount * (flt(frm.doc.percentage) / 100))/flt(frm.doc.avg_rate));
         }
    })
    set_total_weight(frm);
    
 }

 function set_total_weight(frm) {
    var total_weight = 0;
    frm.doc.items.forEach(d => {
        if (flt(d.weight) > 0) {
            total_weight += d.weight;
        }
    })
    frm.set_value("total_weight", total_weight);
}