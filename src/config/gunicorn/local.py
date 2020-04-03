import multiprocessing

max_requests = 50000
max_requests_jitter = 500
reload = True
proc_name = 'src.app:application'
workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:8000'
worker_class = 'sync'
