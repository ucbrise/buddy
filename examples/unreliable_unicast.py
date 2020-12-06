addr: globals
uuid: globals
public: globals
view: globals

Channel: 'function'
Table: 'function'

data_buff = Table(key='@dst', value=('uuid','payload'))
pipe_out = View(query="""
            SELECT *
            FROM data_buff
            WHERE dst = @addr
            """)
ackd = Table(key='dst', value=('uuid', 'payload'))

def ack():
    global ackd
    ackd += pipe_out

@public
def send(dst: str, payload: str):
    global data_buff
    data_buff += {(dst, payload)}

@garbage_collect
def gc():
    global data_buff
    # Application Specific... in CIDR paper, it's
    data_buff -= ackd
    ackd.clear()
