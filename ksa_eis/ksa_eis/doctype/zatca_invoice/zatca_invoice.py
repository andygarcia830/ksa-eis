# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
import subprocess
import requests
import json
import qrcode
import os

from frappe.model.document import Document
from frappe.utils import get_site_base_path

class ZATCAInvoice(Document):
	pass


@frappe.whitelist()
def populate_xml(f):
	doc_root='/home/andy/frappe-bench/sites/erpnext'
	f=doc_root+f
	print(f'\n\nPROCESSING {f}\n\n')
	x=''
	try:
		fl = open(f, "r")
		x=fl.read()
		fl.close()
	except:
		pass
	return x

@frappe.whitelist()
def process_file(f):
	doc_root=get_site_base_path()
	f=doc_root+f
	cmd=f'../apps/ksa_eis/ksa_eis/services/process_files.sh {f}'
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
	doc_root=get_site_base_path()
	f=doc_root+f
	t = f +'.json'
	cmd=f'../apps/ksa_eis/ksa_eis/services/generate_json.sh {f} {t}'
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
	doc_root=get_site_base_path()
	f=doc_root+f
	t = f +'.json'
	cmd=f'../apps/ksa_eis/ksa_eis/services/generate_qr.sh {f} {t}'
	print(f'\n\nPROCESSING {f}')
	print(f'COMMAND={cmd}\n\n')
	result= str(subprocess.check_output(cmd,shell=True))
	result=result[2:-3]
	resultArr=result.split()
	result = resultArr[-1]
	print(result)
	return result

def checkdir(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)

@frappe.whitelist()
def generate_qr_image(qrString,fileName):
	docRoot='./assets/zatca_qrcode/'
	# make sure the directory exists!
	checkdir(docRoot)
	fileName=docRoot+fileName+".png"
	print('\n\n\ngenerating QR Image in '+fileName)
	img = qrcode.make(qrString)
	type(img)  # qrcode.image.pil.PilImage
	img.save(fileName)


if __name__ == '__main__':
	generate_qr_image('test','testqr.png')