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
	gcloud asset search-all-resources --scope=projects/$project | grep assetType | awk '{print $NF}' >> $STATISTICS_FILE
done
