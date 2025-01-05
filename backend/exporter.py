import random
import time
from flask import Flask
from prometheus_client import start_http_server, generate_latest, Gauge, Summary, Counter, Histogram

app = Flask(__name__)

HTTP_REQUESTS=Counter('HTTP_requests_Total', 'Total HTTP request amount', ['endpoint','method', 'code'])
AUTHENTICATED_USERS=Counter('Authenticated_users_requests_total', 'authenticated users count')
HTTP_REQUESTS_LATENCY=Histogram('HTTP_requests_duration_total', 'Histogram to show request latency', ['endpoint','method'])

@app.get('/metrics') # The default Prometheus HTTP path to pull data from
def metrics():
    start_time = time.time()
    HTTP_REQUESTS.labels(endpoint='/metrics', method='get', code='200').inc(1)
    duration = time.time()- start_time
    HTTP_REQUESTS_LATENCY.labels(endpoint='/metrics', method='get').observe(duration)
    return generate_latest()

@app.get('/login')
def login():
    if random.randint(0, 100) > 50:
        HTTP_REQUESTS.labels(endpoint='/login', method='get', code='200').inc(1)
        return '200'
    else:
        HTTP_REQUESTS.labels(endpoint='/login', method='get', code='400').inc(1)
        return '400'


app.run(port=5001, host='0.0.0.0')