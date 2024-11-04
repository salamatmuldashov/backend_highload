from rest_framework.views import APIView
from rest_framework.response import Response
import urllib3
from urllib3.exceptions import HTTPError

http = urllib3.PoolManager()

def quorum_read(key):
    instances = ['http://127.0.0.1:8100/api/data/', 'http://127.0.0.1:8200/api/data/']
    responses = []
    for instance in instances:
        try:
            response = http.request('GET', f'{instance}?key={key}')
            if response.status == 200:
                responses.append(urllib3.util.make_headers().decode(response.data)['value'])
        except HTTPError as e:
            print(f"Request failed: {e}")

    # Simple majority quorum:
    if len(responses) > len(instances) // 2:
        return max(set(responses), key=responses.count)  # Return the most frequent value
    else:
        return None  # Or handle the case where no quorum is reached

def quorum_write(key, value):
    instances = ['http://127.0.0.1:8100/api/data/', 'http://127.0.0.1:8200/api/data/']
    success_count = 0
    for instance in instances:
        try:
            response = http.request('POST', instance, fields={'key': key, 'value': value})
            if response.status == 201:
                success_count += 1
        except HTTPError as e:
            print(f"Request failed: {e}")

    # Simple majority quorum:
    if success_count > len(instances) // 2:
        return True  # Write successful
    else:
        return False  # Write failed


