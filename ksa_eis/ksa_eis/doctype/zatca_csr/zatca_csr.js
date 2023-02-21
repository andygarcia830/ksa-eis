// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("ZATCA CSR", {
    refresh(frm){
         frm.add_custom_button(
             __('Generate CSID'),function(){
                 frappe.set_route("zatca-csid", "new",
                 {"csr": frm.doc.name});
             }
         );
        },

    before_save(frm) {
        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_csr.zatca_csr.generate_csr', args:{
            common_name : frm.doc.common_name,
            serial_number:frm.doc.serial_number,
            organization_identifier:frm.doc.organization_identifier,
            organization_unit_name:frm.doc.organization_unit_name,
            organization_name:frm.doc.organization_name,
            country_name:frm.doc.country_name,
            invoice_type:frm.doc.invoice_type,
            location_address:frm.doc.location_address,
            industry_business_category:frm.doc.industry_business_category
            },
            callback:function(r){
                console.log(r.message)
                frm.doc.csr=r.message
            }
        }
        ).then(r => {
            console.log(r.message)
        })

        
 	}
 });
