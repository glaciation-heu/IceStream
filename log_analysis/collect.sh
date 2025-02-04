#!/bin/bash

curl -X POST "http://grafana.integration/api/ds/query?ds_type=loki&requestId=Q109_1" \
    -H "Content-Type: application/json" \
    -d '{
            "queries":[
	        {"datasource":{
		    "type":"loki",
		    "uid":"P8E80F9AEF21F6940"
	            },
		    "editorMode":"code",
		    "expr":"{namespace=~\"dkg-engine\", container =~\"metadata-service\"} |= \"\"",
		    "queryType":"range",
		    "refId":"A",
		    "maxLines":1000,
		    "legendFormat":"",
		    "datasourceId":2,
		    "intervalMs":30000,
		    "maxDataPoints":567}
            ],
	    "from":"1738638979765",
	    "to":"1738660579765"
        }' \
    -o "logs/$(date +%Y%m%d_%H%M%S).json"

