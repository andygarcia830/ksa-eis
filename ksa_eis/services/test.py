import subprocess
import frappe

import sys


@frappe.whitelist()
def test():
    output=str(subprocess.check_output('source /home/andy/frappe-bench/apps/ksa_eis/ksa_eis/services/test.sh',shell=True))
    print(output)


if __name__ == '__main__':
    test()