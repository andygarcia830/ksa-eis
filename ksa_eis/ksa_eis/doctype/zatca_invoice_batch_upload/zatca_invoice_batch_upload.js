// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("ZATCA Invoice Batch Upload", {
 	before_save(frm) {
        console.log("PROCESSING BATCH UPLOAD")
        //if (frm.doc.status == "REPORTED") return;
        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice_batch_upload.zatca_invoice_batch_upload.process_batch', args:{
            zatca_csid : frm.doc.csid,
            f : frm.doc.xml_file,
            type : frm.doc.invoice_type,
            auto_report: frm.doc.auto_report
            },
            callback:function(r){
                frm.doc.xml_file=""
            }

        });

 	},
 });
