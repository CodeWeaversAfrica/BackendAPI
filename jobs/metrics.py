# jobsapp/metrics.py
from prometheus_client import Counter, Gauge

# Define metrics
requests_total = Counter(
    'api_requests_total',
    'Total number of HTTP requests by endpoint, method, and user.',
    ['endpoint', 'method', 'user']
)

last_user_activity_time = Gauge(
    'api_last_user_activity_time_seconds',
    'The last time a user was active (in seconds since epoch).',
    ['user']
)
