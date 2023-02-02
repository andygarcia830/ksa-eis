// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("ZATCA Invoice", {
    
    refresh(frm) {
        if(frm.doc.status != "REPORTED") frm.add_custom_button(
            __('Submit Report to ZATCA'),function(){
                frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.submit_report', args:{
                    csid : frm.doc.zatca_csid,
                    jsn : frm.doc.json_request
                    },
                    callback:function(r){
                        console.log("REPORT RESULT:"+r.message)
                        frm.doc.status_message=r.message
                        frm.doc.status="REPORTED"
                        frm.dirty()
                        frm.save()
                    }

                });
            }
        );
        console.log("GENERATE QR")
        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.generate_qr_image', args:{
            qrString : 'hello',
            fileName : 'Test_QR.png'
            },
            callback:function(r){
               
            }

        });
        
       
    },

    before_save(frm) {
        console.log("INVOICE SAVE")
        //if (frm.doc.status == "REPORTED") return;
        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.generate_qr', args:{
            f : frm.doc.xml_file
            },
            callback:function(r){
               frm.doc.qr_code_text=r.message
               // GENERATE AND LOAD QR IMAGE
               frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.generate_qr_image', args:{
                    qrString : frm.doc.qr_code_text,
                    fileName : frm.doc.name
                    },
                    callback:function(r){
                    frm.doc.qr_code="/assets/zatca_qrcode/"+frm.doc.name+".png"
                    }
    
                });

            }

        });

        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.populate_xml', args:{
            f : frm.doc.xml_file,
            },
            callback:function(r){
                console.log(r.message)
                frm.doc.xml_document=r.message
                frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.process_file', args:{
                    f : frm.doc.xml_file,
                    },
                    callback:function(r){
                        console.log(r.message)
                        frm.doc.validation_result=r.message
                        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_invoice.zatca_invoice.generate_json', args:{
                            f : frm.doc.xml_file,
                            },
                            callback:function(r){
                                console.log(r.message)
                                frm.doc.json_request=r.message
                            }
                        })
                    }
                })
            }
        }
        ).then(r => {
            console.log(r.message)



        })

        
 	}
 });
