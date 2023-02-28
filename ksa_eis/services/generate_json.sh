#!/bin/bash

pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        export PATH="${PATH:+"$PATH:"}$1"
    fi
}

export FATOORA_HOME=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Apps
export SDK_CONFIG=../apps/ksa_eis/ksa_eis/zatca-einvoicing-sdk-232-R3.1.8/Configuration/config.json

pathadd  $FATOORA_HOME
pathadd ..apps/ksa_eis/ksa_eis/jre1.8.0_361/bin


echo $1
$FATOORA_HOME/fatoora -invoiceRequest -invoice "$1" -apiRequest "$2"