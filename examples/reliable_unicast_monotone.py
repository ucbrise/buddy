from buddy import Channel, Table
from buddy import garbage_collect, periodic, tick

###############
# The Algorithm
###############

pipe_in = Table(key=('dst', 'src', 'ident'), value='payload', extensional=True)
pipe_sent = Table(key=('dst', 'src', 'ident'), value='payload', extensional=False)


data_chan = Channel(key=('@dst', 'src', 'ident'), value='payload')
ack_chan = Channel(key=('@src', 'dst', 'ident'))

def send_packet():
    global data_chan
    data_chan += pipe_in - pipe_sent

def send_ack():
    global ack_chan
    ack_chan += {(p.src, p.dst, p.ident) for p in data_chan}

def recv_ack():
    global pipe_sent
    # Stratified Negation
    with tick():
        pipe_sent += {s for s in pipe_in for a in ack_chan if s.ident == a.ident}


###################
# The Optimization
###################

@garbage_collect
def forget():
    global pipe_in, pipe_sent
    pipe_in -= pipe_sent
    pipe_sent.clear()

@periodic(s=10)
def timer_retry():
    send_packet()


