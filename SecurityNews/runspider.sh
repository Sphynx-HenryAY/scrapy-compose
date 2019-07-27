#!/bin/bash

if [ $1 ]; then
	scrapy crawl $1 -t json -o $1.json
fi
