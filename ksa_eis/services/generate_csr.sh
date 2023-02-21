#!/bin/bash
export FATOORA_HOME=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Apps
export SDK_CONFIG=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Configuration/config.json
export INPUT_PATH=$1

#command_string="fatoora -csr -csrConfig \"$INPUT_PATH/csr-config.properties\" -generatedCsr \"$INPUT_PATH/generated_csr.csr\""
#echo $command_string
$FATOORA_HOME/fatoora -csr -csrConfig "$INPUT_PATH/csr-config.properties" -generatedCsr "$INPUT_PATH/generated_csr.csr"
