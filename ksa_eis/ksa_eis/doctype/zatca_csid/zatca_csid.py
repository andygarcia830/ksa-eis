# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
import requests
import json

from frappe.model.document import Document

class ZATCACSID(Document):
	pass

def call_compliance(otp,csr):
	url = 'https://gw-apic-gov.gazt.gov.sa/e-invoicing/developer-portal/compliance'
	hdrs = {'accept':'application/json','OTP': str(otp),'Accept-Version':'V2'}
	bdy = {'csr':csr}
	x = requests.post(url, json=bdy, headers=hdrs)
	xArr=json.loads(x.text)
	for item in xArr:
		print(f'{item}={xArr[item]}')
        #print(item)
	return x.text

def call_csid_onboading(csid,secret,jsn):
	url = 'https://gw-apic-gov.gazt.gov.sa/e-invoicing/developer-portal/production/csids'
	#url = 'http://localhost:8000'
	
	hdrs = {'Accept-Language':'en','Accept-Version':'V2'}
	x = requests.post(url, json=jsn, headers=hdrs,auth=(csid,secret))
	xArr=json.loads(x.text)
	for item in xArr:
		print(f'{item}={xArr[item]}')
		#print(item)
	return x.text


@frappe.whitelist()
def generate_csid(otp,csr):
	print(f'\n\n{csr} {otp}\n\n')
	xArr=call_compliance(otp,csr)
	return xArr

@frappe.whitelist()
def fetch_csr(csr):
	print(f'fetching CSR for {csr}')
	doc=frappe.get_doc('ZATCA CSR',csr)
	print(f'fetched doc={doc.csr}')
	return doc.csr

@frappe.whitelist()
def onboard_csid(csid,secret):
	jsn={'compliance_request_id':'1234567890123'}
	print(f'onboard_csid {csid} {secret}')
	return call_csid_onboading(csid,secret,jsn)


