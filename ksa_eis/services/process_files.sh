#!/bin/bash
export PATH=$PATH:/usr/bin
export FATOORA_HOME=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Apps
export SDK_CONFIG=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Configuration/config.json
echo $1
$FATOORA_HOME/fatoora -validate -invoice "$1"