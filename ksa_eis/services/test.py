import subprocess
import frappe

import sys


@frappe.whitelist()
def test():
   # output=str(subprocess.check_output('source ../apps/ksa_eis/ksa_eis/services/test.sh',shell=True))
    output=str(subprocess.check_output('pwd',shell=True))
    print(f'PWD={output}')


if __name__ == '__main__':
    test()