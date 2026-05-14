#!/usr/bin/bash

PROJECTS=$(gcloud asset search-all-resources \
    --scope=organizations/351362023871 \
    --asset-types=cloudresourcemanager.googleapis.com/Project \
    --format="table(additionalAttributes.projectId)" | grep -v PROJECT_ID)

for project in $PROJECTS
do
	number=$(gcloud asset search-all-resources --scope=projects/$project | grep assetType | wc -l)
	echo -e "$project\t$number"
done
