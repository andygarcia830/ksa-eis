# Copyright (c) 2023, Andy Garcia and contributors
# For license information, please see license.txt

# import frappe
import subprocess

from frappe.model.document import Document

class FileProcessor(Document):
	def process_file():
		subprocess.Popen('echo "Geeks 4 Geeks"', shell=True)
