frappe.ui.form.on("Sales Invoice", {

    refresh: function(frm) {
        frm.set_query("hs_code", function() {
            return {
                filters: [
                    ["is_group", "=", 0]
                ]
            };
        });
    },
    work_type: function (frm) {
        set_weight(frm);
    },
    hs_code: function (frm) {
        copy_hs_code_to_child(frm);
    }
   
    
});

frappe.ui.form.on("Sales Invoice Item", {
    qty: function (frm, cdt, cdn) {
        if (flt(frm.doc.avg_rate) > 0) {
            var row = locals[cdt][cdn];
            frappe.model.set_value(cdt, cdn, "weight", (row.amount * (flt(frm.doc.percentage) / 100))/flt(frm.doc.avg_rate));
        }
        set_total_weight(frm);
    },
    items_add: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "hs_code", frm.doc.hs_code);
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
async function copy_hs_code_to_child(frm) {
    const hs = frm.doc.hs_code;
    const res = hs
      ? await frappe.db.get_value("HS Code", { name: hs }, "uom")
      : { message: null };
  
    const parent_uom = res?.message?.uom || "";
    // REVIEW slipperiness: {name: hs} can be replaced with "hs" if that's doc name key
  
    frm.doc.items.forEach(row => {
      frappe.model.set_value(row.doctype, row.name, "hs_code", hs || "");
      frappe.model.set_value(row.doctype, row.name, "fbr_uom", parent_uom);
    });
  
    frm.refresh_field("items");
  }
  