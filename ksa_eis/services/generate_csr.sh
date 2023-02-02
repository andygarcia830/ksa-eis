#!/bin/bash
export PATH=/home/andy/.nvm/versions/node/v10.15.3/bin:/home/andy/.local/bin:/home/andy/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/var/lib/snapd/snap/bin:/home/andy/ssh_scripts:/home/andy/ssh_scripts:/home/andy/Work/KSA-ZATCA-EIS/SDK/zatca-einvoicing-sdk-232-R3.1.8/Apps/:/home/andy/Work/KSA-ZATCA-EIS/SDK/zatca-einvoicing-sdk-232-R3.1.8/Apps/
export FATOORA_HOME=/home/andy/Work/KSA-ZATCA-EIS/SDK/zatca-einvoicing-sdk-232-R3.1.8/Apps
export SDK_CONFIG=/home/andy/Work/KSA-ZATCA-EIS/SDK/zatca-einvoicing-sdk-232-R3.1.8/Configuration/config.json
export INPUT_PATH=/home/andy/frappe-bench/sites/erpnext/private/files

#command_string="fatoora -csr -csrConfig \"$INPUT_PATH/csr-config.properties\" -generatedCsr \"$INPUT_PATH/generated_csr.csr\""
#echo $command_string
fatoora -csr -csrConfig "$INPUT_PATH/csr-config.properties" -generatedCsr "$INPUT_PATH/generated_csr.csr"
