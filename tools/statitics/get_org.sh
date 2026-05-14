#!/usr/bin/bash
infos=$(gcloud organizations get-iam-policy 351362023871 --format=json | jq '.bindings[] | select(.role == "roles/owner" or .role == "roles/editor" or .role == "roles/billing.admin" or .role == "roles/resourcemanager.folderAdmin" or .role == "roles/recommender.iamAdmin" or .role == "roles/resourcemanager.organizationAdmin") | .members[]'| sed 's,",,g')

for i in $infos
do
	type=$(echo $i| awk -F':' '{print $1}')
	email=$(echo $i | awk -F':' '{print $2}')
	lasttime=$(gcloud logging read 'protoPayload.authenticationInfo.principalEmail="'$email'"' --limit=1 --freshness=30d --format="json" --organization=351362023871 | jq '.[].timestamp')
	echo "heytapcloud.com,$type,$email,$lasttime"
done
