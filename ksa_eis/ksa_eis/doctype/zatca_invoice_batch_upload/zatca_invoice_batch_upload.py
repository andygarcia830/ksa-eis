# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
import datetime
import importlib
import requests
import json
import qrcode
import subprocess
import sys
import ksa_eis.ksa_eis.doctype.zatca_csr.zatca_csr

from frappe.model.document import Document
from frappe.utils import get_site_base_path

class ZATCAInvoiceBatchUpload(Document):
	pass

@frappe.whitelist()

def process_batch(zatca_csid,f,type,auto_report):
	print(f'\n\n\AUTO_REPORT={auto_report}\n\n')
	doc_root=get_site_base_path()
	f=doc_root+f
	print(f'\n\nPROCESSING {f}\n\n')
	x=''
	try:
		fl = open(f, "r")
		x=fl.read()
		fl.close()
	except:
		pass
	
	d='<?xml version="1.0" encoding="UTF-8"?>'
	xArr=x.split(d)
	print(f'xArr size={len(xArr)}')
	ctr=0
	now=datetime.datetime.now()
	dt=now.strftime("%Y-%m-%m-%H:%M:%S")
	for entry in xArr:
		if (len(entry)>0):
			process_doc(f,ctr,f'{d}\n{entry}',dt,zatca_csid,type,auto_report)
		ctr+=1


def process_doc(f,ctr,entry,dt,csid,type,auto_report):
	f=f'{f}.{dt}.{ctr}'
	try:
		fl = open(f, "w")
		x=fl.write(entry)
		fl.close()
	except:
		pass
	doc = frappe.new_doc('ZATCA Invoice')
	doc.title = "EIS-BATCH-"+dt+"-"+str(ctr)
	doc.xml_document=entry
	doc.zatca_csid=csid
	doc.xml_file=f
	doc.invoice_type=type
	doc.status='UNREPORTED'
	r=process_file(f)
	print('VALIDATION RESULT='+r)
	doc.validation_result=str(r)
	r=generate_json(f)
	print('JSON='+r)
	doc.json_request=r
	r=generate_qr(f)
	print('QR='+r)
	doc.qr_code_text=r
	fArr=f.split('/')
	fileName=fArr[-1]
	print('FILENAME='+fileName)
	generate_qr_image(doc.qr_code_text,fileName)
	doc.qr_code='/assets/zatca_qrcode/'+fileName+'.png'
	if auto_report == '1':
		doc.status='REPORTED'
		r=submit_report(csid,doc.json_request)
		doc.status_message=r
	doc.insert()
	

def process_file(f):
	cmd=f'source ../apps/ksa_eis/ksa_eis/services/process_files.sh {f}'
	print(f'\n\nPROCESSING {f}')
	print(f'COMMAND={cmd}\n\n')
	result= str(subprocess.check_output(cmd,shell=True))
	print(result)
	resultArr=extract_validate_results(result)
	print(resultArr)
	return resultArr

def extract_validate_results(result ):
 # Clean up and format result
	result=result[2:-1]
	resultArr=result.split('\\r\\n')
	lastLine=resultArr[-1]
	resultArr=lastLine.split('\\n')
	print(f"resultArr size={len(resultArr)}\n")
	resultRet = ''
	for line in resultArr:
		if line.find('ValidationProcessorImpl') > 1:
			resultRet+=line
			resultRet+='\n'
		else: 
			continue
	print(f"resultRet size={len(resultRet)}\n")
	return resultRet

@frappe.whitelist()
def generate_json(f):
	t = f +'.json'
	cmd=f'source ../apps/ksa_eis/ksa_eis/services/generate_json.sh  {f} {t}'
	print(f'\n\nPROCESSING {f}')
	print(f'COMMAND={cmd}\n\n')
	result= str(subprocess.check_output(cmd,shell=True))
	print(result)
	print(f'\n\READONG TARGET JSON {t}')
	try:
		fl = open(t, "r")
		x=fl.read()
		fl.close()
	except:
		pass
	return x

@frappe.whitelist()
def submit_report(csid,jsn):
	doc=frappe.get_doc('ZATCA CSID',csid)
	print(f'USING CSID={doc.prod_csid} secret={doc.prod_secret}')
	jsnArr=json.loads(jsn)
	url = 'https://gw-apic-gov.gazt.gov.sa/e-invoicing/developer-portal/invoices/reporting/single'
	#url = 'http://localhost:8000'
	hdrs = {'Accept-Language':'en','Accept-Version':'V2','Clearance-Status':'0'}
	x = requests.post(url, json=jsnArr, headers=hdrs,auth=(doc.prod_csid,doc.prod_secret))
	#x = requests.post(url, json=jsn, headers=hdrs)
	print(x.raise_for_status)
	print(x.text)
	xArr=json.loads(x.text)
	resultStr=''
	for item in xArr:
		print(f'{item}={xArr[item]}')
		resultStr+=item
		resultStr+='='
		resultStr+=str(xArr[item])
		resultStr+='\n'
	print(f'resultStr={resultStr}')
	return resultStr

@frappe.whitelist()
def generate_qr(f):
	t = f +'.json'
	cmd=f'source ../apps/ksa_eis/ksa_eis/services/generate_qr.sh {f} {t}'
	print(f'\n\nPROCESSING {f}')
	print(f'COMMAND={cmd}\n\n')
	result= str(subprocess.check_output(cmd,shell=True))
	result=result[2:-3]
	resultArr=result.split()
	result = resultArr[-1]
	print(result)
	return result



@frappe.whitelist()
def generate_qr_image(qrString,fileName):
	docRoot='./assets/zatca_qrcode/'
	fileName=docRoot+fileName+".png"
	print('\n\n\ngenerating QR Image in '+fileName)
	img = qrcode.make(qrString)
	type(img)  # qrcode.image.pil.PilImage
	img.save(fileName)


