#!/bin/bash

# 设置 project 名称
project=oppo-gcp-prod
# 存储获取项目中所有 vm 的相关信息临时文件
tmpfile=diskinfo.txt

# 没有指定的 label 写入到 error.log
error_log=error.log

gcloud compute instances list --project=$project --format=json | \
	jq -r '.[] | {name: .name, zone: .zone, disks: .disks[].source, psa_product_id: .labels.psa_product_id} | join(" ")' > $tmpfile

while read -r name zone disk label
do
	if [ -z "$name" ] || [ -z "$label" ] || [ -z "$zone" ] || [ -z "$disk" ]
	then
		echo -ne "name=$name\tlabel=$label\tzone=$zone\tdisk=$disk\n" >> error.log
		continue
	fi
	zone=$(basename $zone)
	disk=$(basename $disk)
	# 打印出要执行的命令，如果要真正执行把 echo 和双引号删除即可
	echo "gcloud compute disks update $disk --update-labels=psa_product_id=$label --project=$project --zone=$zone"
done < $tmpfile
