import urllib.request

req = urllib.request.Request('http://127.0.0.1:8003/history')
try:
    urllib.request.urlopen(req)
    print('unauthorized-ok')
except Exception as exc:
    print(type(exc).__name__, getattr(exc, 'code', ''))
