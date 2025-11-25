import urllib.request
import time

url = 'http://127.0.0.1:8000/'
for i in range(10):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            status = r.getcode()
            body = r.read(2048)
            print(f'STATUS: {status}')
            print('BODY_SNIPPET:')
            print(body.decode('utf-8', errors='replace')[:1000])
            raise SystemExit(0)
    except Exception as e:
        print(f'attempt {i+1}: {e}')
        time.sleep(0.6)
print('failed to reach server')
raise SystemExit(2)
