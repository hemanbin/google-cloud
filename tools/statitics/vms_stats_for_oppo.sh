#!/usr/bin/bash

PROJECTS=$(gcloud asset search-all-resources \
    --scope=organizations/351362023871 \
    --asset-types=cloudresourcemanager.googleapis.com/Project \
    --format="table(additionalAttributes.projectId)" | grep -v PROJECT_ID)

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"

DATA_DIR=$(realpath "${BIN_DIR}/../data")

TIMESTAMP=$(date "+%Y-%m-%d-%H")

STATISTICS_FILE="${DATA_DIR}/vms_${TIMESTAMP}"


for project in $PROJECTS
do
	gcloud services list --project=$project| grep compute.googleapis.com > /dev/null
	enable=$?
	if [ $enable -eq 0 ]
	then
		#echo $project >> $STATISTICS_FILE
		#gcloud compute instances list --project=$project --filter="status=RUNNING" --format="value(name.basename(), zone.basename(), machineType.basename())" >> $STATISTICS_FILE
		gcloud compute instances list --project=$project --filter="status=RUNNING" --format="value(zone.basename(), machineType.basename())" \
			| sed 's,-a\t,\t,g' | sed 's,-b\t,\t,g' | sed 's,-c\t,\t,g' | sed 's,-d\t,\t,g' >> $STATISTICS_FILE
	fi
done
