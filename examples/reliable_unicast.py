# State-based CRDT.

data_buff = Table(key='@dst', value=('uuid','payload'))
pipe_in = View(query="""
            SELECT *
            FROM data_buff
            WHERE dst = addr()
            """)
ackd = Table(key='dst', value=('uuid', 'payload'))

def ack():
    global ackd
    ackd += pipe_in

@public
def send(dst: str, payload: str):
    global data_buff
    data_buff += {(dst, uuid(), payload)}

@garbage_collect
def gc():
    global data_buff
    # Application Specific... in CIDR paper, it's
    data_buff -= ackd
    ackd.clear()
