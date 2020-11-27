import pysqldf
import time
from buddy import Channel
from buddy import init

###############
# The Algorithm
###############

connect = Channel(key=('@addr', 'client'), value='nick')
mcast = Channel()

def multicast():
    global mcast
    mcast += [n.key, m.val for m in mcast for n in [c.client, c.nick for c in connect]]


###################
# The Schedule
###################

@init
def run(nick, port, server):
    global connect, mcast
    connect += [[server, port, nick]]
    while True:
        mcast += [server, [port, nick, time(), input('Message: ')]]
        print([m.val for m in mcast])
