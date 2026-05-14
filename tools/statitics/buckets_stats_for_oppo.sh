#!/usr/bin/bash

PROJECTS=$(gcloud asset search-all-resources \
    --scope=organizations/351362023871 \
    --asset-types=cloudresourcemanager.googleapis.com/Project \
    --format="table(additionalAttributes.projectId)" | grep -v PROJECT_ID)

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"

DATA_DIR=$(realpath "${BIN_DIR}/../data")

TIMESTAMP=$(date "+%Y-%m-%d")

STATISTICS_FILE="${DATA_DIR}/bucket_${TIMESTAMP}"

TMP_FILE=/tmp/bucket_info.tmp

AUTH_INFO=$(gcloud auth application-default print-access-token)

for project in $PROJECTS
do
	gcloud services list --project=$project| grep 'storage.googleapis.com' > /dev/null
	enable=$?
	if [ $enable -eq 0 ]
	then
		for bucket in `gcloud storage ls --project=$project`
		do
			bucket=$(echo $bucket | sed 's,gs://,,g' | sed 's,/$,,g')
			psa=$(gcloud storage buckets describe gs://${bucket} --format="value(labels.psa_product_name)" --project=${project})
			curl -H "Authorization: Bearer ${AUTH_INFO}" "https://monitoring.googleapis.com/v3/projects/$project/timeSeries?filter=metric.type=%22storage.googleapis.com/storage/total_bytes%22%20AND%20resource.label.bucket_name%3D%22${bucket}%22&interval.endTime=${TIMESTAMP}T00:05:00Z&interval.startTime=${TIMESTAMP}T00:00:00Z" > $TMP_FILE 
			size=$(cat $TMP_FILE | jq '.timeSeries[].points[].value.doubleValue' | tail -n 1)
			region=$(cat $TMP_FILE | jq '.timeSeries[].resource.labels.location'| tail -n 1)
			echo -e "$project\t$bucket\t$psa\t$region\t$size" >> $STATISTICS_FILE
		done
	fi
done

rm $TMP_FILE
