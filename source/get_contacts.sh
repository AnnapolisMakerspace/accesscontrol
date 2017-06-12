#!/bin/bash

#>&2 echo "starting up..."

WILD_APRICOT_API_KEY=$1
#WILD_APRICOT_API_KEY="<---redacted--->"

b64key=$(echo "APIKEY:${WILD_APRICOT_API_KEY}" | base64)

# >&2 echo "base64 encoded API key:  ${b64key}"
# >&2 echo "setting request data..."

req_data='grant_type=client_credentials&scope=contacts_view'

auth_resp=$(curl -s \
	-H "Authorization: Basic $b64key" \
	-d $req_data \
	https://oauth.wildapricot.org/auth/token
)

#>&2 echo $auth_resp | jq .

auth_token=$(echo $auth_resp | jq -c -r '.access_token')
account_number=$(echo $auth_resp | jq '.Permissions[0].AccountId')

# >&2 echo "auth_token: ${auth_token}"
# >&2 echo "account_number: ${account_number}"

echo $(curl -s \
	 -G \
	 -H "Authorization: Bearer $auth_token" \
	 "https://api.wildapricot.org/v2.1/Accounts/${account_number}/Contacts" \
	 -d '$async=false')
