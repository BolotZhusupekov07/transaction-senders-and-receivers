import gevent.monkey

gevent.monkey.patch_all()


bind = "0.0.0.0:8000"

timeout = 600

log_level = "debug"
access_logfile = "-"

workers = 2
worker_class = "gevent"
worker_connections = 1000
