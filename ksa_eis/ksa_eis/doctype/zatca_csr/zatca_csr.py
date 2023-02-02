# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

import frappe
import subprocess 

from frappe.model.document import Document

class ZATCACSR(Document):
	pass

@frappe.whitelist()

def generate_csr(common_name,serial_number,organization_identifier,organization_unit_name,organization_name,country_name,invoice_type,location_address,industry_business_category):
	#print(f'\n\n{common_name}\n{serial_number}\n{organization_identifier}\n{organization_unit_name}\n{organization_name}\n{country_name}\n{invoice_type}\n{location_address}\n{industry_business_category}\n\n\n')
	properties=f'csr.common.name={common_name}\ncsr.serial.number={serial_number}\ncsr.organization.identifier={organization_identifier}\ncsr.organization.unit.name={organization_unit_name}\ncsr.organization.name={organization_name}\ncsr.country.name={country_name}\ncsr.invoice.type={invoice_type}\ncsr.location.address={location_address}\ncsr.industry.business.category={industry_business_category}\n'
	print(properties)
	f = open("./erpnext/private/files/csr-config.properties", "w")
	f.write(properties)
	f.close()
	result= str(subprocess.check_output('source /home/andy/frappe-bench/apps/ksa_eis/ksa_eis/services/generate_csr.sh',shell=True))
	print(result)
	f = open("./erpnext/private/files/generated_csr.csr", "r")
	csr=f.read()
	f.close()
	return csr

