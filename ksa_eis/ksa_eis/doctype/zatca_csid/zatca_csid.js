// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("ZATCA CSID", {
    
    before_save(frm) {
        let csr='';
        console.log("CSR1="+csr)
        console.log("calling fetch_csr")
        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_csid.zatca_csid.fetch_csr', args:{
            csr:frm.doc.csr
            },
            callback:function(r){
                console.log(r.message)
                csr=r.message
                console.log("CSR2="+csr)
                frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_csid.zatca_csid.generate_csid', args:{
                    otp:frm.doc.otp,
                    csr:csr
                    },
                    callback:function(r){
                        let msg=r.message
                        console.log(msg)
                        let jsonDoc=JSON.parse(msg)
                        console.log("jsonDoc="+jsonDoc.requestID)
                        frm.doc.csid=jsonDoc.binarySecurityToken
                        frm.doc.secret=jsonDoc.secret
                        frm.doc.status=jsonDoc.dispositionMessage
                        console.log("calling onboard_csid")

                        frappe.call({method:'ksa_eis.ksa_eis.doctype.zatca_csid.zatca_csid.onboard_csid', args:{
                            csid:frm.doc.csid,
                            secret:frm.doc.secret
                            },
                            callback:function(r2){
                                console.log(r2.message)
                                let msg2=r2.message
                                let jsonDoc2=JSON.parse(msg2)
                                console.log("jsonDoc2="+jsonDoc2.requestID+"."+jsonDoc2.secret)
                                frm.doc.prod_csid=jsonDoc2.binarySecurityToken
                                frm.doc.prod_secret=jsonDoc2.secret
                            }
        }
        )
                    }
                }
                )

            }
        }
        )
        




        
 	}
 });
