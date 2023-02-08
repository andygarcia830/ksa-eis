import datetime

import sys
#sys.path.append('/home/andy/frappe-bench/apps/ksa_eis/ksa_eis/ksa_eis/doctype/zatca_csr')
sys.path.append('ksa_eis/ksa_eis/doctype/zatca_csr')
import zatca_csr

now=datetime.datetime.now()
n=now.strftime("%Y/%m/%m-%H:%M:%S")
print(n)