#!/usr/bin/env python

import sys
import redis
from optparse import OptionParser

stats = {'total_connections_received': 0, 'connected_clients': 0, 'used_memory': 0, 'total_commands_processed': 0, 
         'keys': 0, 'expires': 0}

parser = OptionParser(usage="usage: %prog [-h] [-p PORT] [-d DB] [-a AUTH_PASSWORD ] HOSTNAME ...")
parser.set_defaults(port = "6379")
parser.add_option("-p", "--port", dest="port", metavar="PORT",
                  help="default memcached port [default: 6379]")
parser.set_defaults(db = "db0")
parser.add_option("-d", "--db", dest="db", metavar="DB",
                  help="redis database [default: db0]")
parser.set_defaults(auth = "")
parser.add_option("-a", "--auth", dest="auth", metavar="AUTH",
                  help="auth password [default: '']")
(options, args) = parser.parse_args()

hosts = []
if (args):
    host=args[0]
else:
    parser.error("HOSTNAME is required.")
    sys.exit(1)

r = redis.Redis(host=host, port=int(options.port), db=0, password=options.auth)
redis_info = r.info()

if(not redis_info):
  sys.exit()

if(options.db in redis_info):
  db_info = redis_info[options.db]
  for k in db_info:
    if(k in stats):
      stats[k] = int(db_info[k])


for k, v in stats.iteritems():
  if(k in redis_info):
    v = int(redis_info[k])
  print "%s:%s" % (k, v),
