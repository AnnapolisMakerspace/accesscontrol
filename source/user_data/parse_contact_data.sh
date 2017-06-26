#!/bin/bash

pretty_jq_expression='
	.Contacts[] | {
		"name": .DisplayName,
		"status": .Status,
		"userId": .Id,
		"rfid": (.FieldValues[] | select(.FieldName=="RFID") | .Value)
	}
'

function join_by { local IFS="$1"; shift; echo "$*"; }
jq_expression=$(join_by '' ${pretty_jq_expression})

while read l;
do
	echo $l | \
		jq -c -r ${jq_expression}
done
