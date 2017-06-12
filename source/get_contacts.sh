#!/bin/bash
#>&2 echo "starting up..."

WILD_APRICOT_API_KEY=$1
#WILD_APRICOT_API_KEY="<---redacted--->"


# Usage:
# $ get_contacts.sh $API_KEY > /path/to/contact_data.json


# Interacting with the WildApricot API is not terribly convenient.
# This isn't necessarily a bad thing, but if you're unfamiliar
# OAuth tokens it may seems as though there are a number of
# hoops that we need to jump through.

# Let's begin:
# we need to base64 encode the authentication string.
# (when using the API key, 'username' is 'APIKEY', as shown)
b64key=$(echo "APIKEY:${WILD_APRICOT_API_KEY}" | base64)
# >&2 echo "base64 encoded API key:  ${b64key}"


# we need to request a token from wildapricot's OAuth API.
# in this case, we're also going to limit the scope of the
# token we're requesting, to "contacts_view" only:
req_data='grant_type=client_credentials&scope=contacts_view'


auth_resp=$(curl -s \
	-H "Authorization: Basic $b64key" \
	-d $req_data \
	https://oauth.wildapricot.org/auth/token
)
#>&2 echo $auth_resp | jq .

# auth_resp will look like this:
#
#     {
#       "access_token": "<access-token>",
#       "token_type": "Bearer",
#       "expires_in": 1800,
#       "refresh_token": "<refresh-token>",
#       "Permissions": [
#         {
#           "AccountId": <account-number>,
#           "AvailableScopes": [
#             "contacts_view"
#           ]
#         }
#       ]
#     }
#

# grab the needed values out of the json response:
auth_token=$(echo $auth_resp | jq -c -r '.access_token')
account_number=$(echo $auth_resp | jq '.Permissions[0].AccountId')

# >&2 echo "auth_token: ${auth_token}"
# >&2 echo "account_number: ${account_number}"

# and finally, 
echo $(curl -s \
	-G \
	-H "Authorization: Bearer $auth_token" \
	"https://api.wildapricot.org/v2.1/Accounts/${account_number}/Contacts" \
	-d '$async=false'
)

# note that we're not passing a ~variable~ "async",
# the URL parameter that wildapricot expects is the
# actual ~string~: '$async'
