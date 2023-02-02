// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("File Processor", {
 	refresh(frm) {
        frappe.call({
            method:'ksa_eis.services.ksa_eis_processor.process_file',
            asgs:[]
        }
        )
 	},
 });
