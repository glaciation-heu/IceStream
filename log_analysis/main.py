import re
import requests
import argparse
import json
import pandas as pd
import urllib.parse

from datetime import datetime, timedelta


def get_logs(url: str, data: str) -> dict:
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(
        url,
        json=data,
        headers=headers
    )
    if res.status_code == 200:
        return res.json()
    else:
        print(res)
        return None


def process_json(res: dict) -> pd.DataFrame:
    if res:
        loglines = res['results']['A']['frames'][0]['data']['values'][2]
        timestamps, queries = list(), list()
        for l in loglines:
            match = re.search(r'\?query=([^\s]+)', l)
            if match:
                timestamps.append(l.split(' ')[0].strip())
                encoded_query = match.group(1)
                decoded_query = urllib.parse.unquote(encoded_query).replace('+',' ')
                queries.append(decoded_query.strip().replace('\n', ' '))
        
        # To file
        assert len(timestamps) == len(queries)
        with open('logs/timestamps.txt', 'a+') as f:
            for t in timestamps:
                f.write(t + '\n')
        with open('logs/queries.txt', 'a+') as f:
            for q in queries:
                f.write(q + '\n')
    else:
        print('None successful request')


def main():
    parser = argparse.ArgumentParser(description='Loki log collect and process')
    parser.add_argument(
        '--url', 
        help='Then endpoint to send the request',
        default='http://grafana.integration/api/ds/query?ds_type=loki&requestId=Q109_1'
    )
    args = parser.parse_args()

    # Prepare time range for request
    cur_tmp = datetime.now()
    hr_ago = int((cur_tmp - timedelta(hours=1)).timestamp()*1000)
    cur_tmp = int(cur_tmp.timestamp()*1000)

    data = {
            "queries": [
                {
                    "datasource": {
                        "type": "loki",
                        "uid": "P8E80F9AEF21F6940"
                    },
                    "editorMode": "code",
                    "expr": "{namespace=~\"dkg-engine\", container =~\"metadata-service\"} !~ \"DEBUG\"",
                    "queryType": "range",
                    "refId": "A",
                    "maxLines": 5000,
                    "legendFormat":"", 
                    "datasourceId":2,
                    "intervalMs":30000,
                    #"maxDataPoints":567
                    }
            ],
            "from": str(hr_ago),
            "to": str(cur_tmp)
    }

    # Request Grafana DS endpoint to get logs
    res = get_logs(args.url, data)

    # Filter relevant part to get timestamp, query
    process_json(res)


if __name__ == '__main__':
    main()
