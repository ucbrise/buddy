import pysqldf
from buddy import Channel, Table, Interface
from buddy import periodic


pipe_in = Interface(key=('dst', 'src', 'ident'), value=('payload'))
pipe_sent = Interface(key=('dst', 'src', 'ident'), value=('payload'))

data_chan = Channel(key=('@dst', 'src', 'ident'), value=('payload'))
ack_chan = Channel(key=('@src', 'dst', 'ident'))
send_buf = Table(key=('dst', 'src', 'ident'), value=('payload'))

def send_packet():
    global send_buf, data_chan
    send_buf += pipe_in
    data_chan += pipe_in

def timer_retry():
    global data_chan
    while periodic(timer=10):
        data_chan += send_buf

def send_ack():
    global ack_chan
    ack_chan += [p.src, p.dst, p.ident for p in data_chan]


def recv_ack():
    global pipe_sent, send_buf
    got_ack = [s for s in send_buf for a in ack_chan if s.ident == a.ident]
    pipe_sent += got_ack
    send_buf = pysqldf(
        """
        SELECT *
        FROM send_buf
        EXCEPT
        SELECT *
        FROM got_ack
        """
    )
    

