#!/usr/bin/bash

PROJECTS=$(gcloud asset search-all-resources \
    --scope=organizations/351362023871 \
    --asset-types=cloudresourcemanager.googleapis.com/Project \
    --format="table(additionalAttributes.projectId)" | grep -v PROJECT_ID)

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"

DATA_DIR=$(realpath "${BIN_DIR}/../data")

TIMESTAMP=$(date "+%Y-%m-%d")

STATISTICS_FILE="${DATA_DIR}/vms_${TIMESTAMP}"

for project in $PROJECTS
do
	infos=$(gcloud projects get-iam-policy $project --format=json | jq '.bindings[] | select(.role == "roles/owner" or .role == "roles/editor") | .members[]' | sed 's,",,g')
	for i in $infos
	do
		type=$(echo $i| awk -F':' '{print $1}')
		email=$(echo $i | awk -F':' '{print $2}')
		if [ $type == 'serviceAccount' ]
		then
			keys=$(gcloud iam service-accounts keys list --iam-account=$email --managed-by=user --project=$project | wc -l)
			if [ $keys -eq 0 ]
			then
				continue
			fi
		fi
		lasttime=$(gcloud logging read 'protoPayload.authenticationInfo.principalEmail="'$email'"' --limit=1 --freshness=90d --format="json" --project=$project | jq '.[].timestamp')
		echo "$project,$type,$email,$lasttime"
	done
done
