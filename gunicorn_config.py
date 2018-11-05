worker_class = 'gevent'
worker_connections = 25
workers = 1

def pre_fork(server, worker):
    import gevent.monkey
    import psycogreen.gevent
    gevent.monkey.patch_all()
    print('Making code green')
    psycogreen.gevent.patch_psycopg()
    print('Making psycopg green')