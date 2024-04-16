# FOR PRODUCTION
# broker_url = 'redis://redis:6379/0'
# result_backend = 'redis://redis:6379/0'

# FOR LOCAL TESTING
broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/0'

imports = ('main', 'objects.reservation')
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'

task_routes = {
    'main.get_token': {'queue': 't', 'routing_key': 't'},
    'main.book': {'queue': 'b', 'routing_key': 'b'}
}

worker_pool = 'gevent'
worker_concurrency = 20
task_soft_time_limit = 300
task_time_limit = 600
