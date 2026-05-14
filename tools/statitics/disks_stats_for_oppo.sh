#!/usr/bin/bash

PROJECTS=$(gcloud asset search-all-resources \
    --scope=organizations/351362023871 \
    --asset-types=cloudresourcemanager.googleapis.com/Project \
    --format="table(additionalAttributes.projectId)" | grep -v PROJECT_ID)

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"

DATA_DIR=$(realpath "${BIN_DIR}/../data")

TIMESTAMP=$(date "+%Y-%m-%d")

STATISTICS_FILE="${DATA_DIR}/disk_${TIMESTAMP}"


for project in $PROJECTS
do
	gcloud services list --project=$project| grep compute.googleapis.com > /dev/null
	enable=$?
	if [ $enable -eq 0 ]
	then
		gcloud compute disks list --project=$project --filter="status=READY" --format="value(location(), sizeGb, type.basename())" \
			| sed 's,-a,,g' | sed 's,-b,,g' | sed 's,-c,,g' | sed 's,-d,,g' >> $STATISTICS_FILE
	fi
done
