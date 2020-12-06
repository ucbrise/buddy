messages = Table(key=('sender', 'port', 'nick', 'timestamp'), value='msg')

@public
def send(server:str, port:int, nick: str, msg: str):
    global messages
    messages += {(server, port, nick, time(), msg)}
