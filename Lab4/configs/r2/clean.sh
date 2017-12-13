#!/bin/sh

# This script clear the logs
varpath='/home/lca2/Desktop/shared/lab4/configs/r2'

rm $varpath/logs/zebra.log
touch $varpath/logs/zebra.log
chmod 666 $varpath/logs/zebra.log

rm $varpath/logs/ospfd.log
touch $varpath/logs/ospfd.log
chmod 666 $varpath/logs/ospfd.log

rm $varpath/logs/ospf6d.log
touch $varpath/logs/ospf6d.log
chmod 666 $varpath/logs/ospf6d.log

/etc/init.d/quagga restart

