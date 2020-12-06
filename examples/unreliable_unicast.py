comm = Channel(key='@dst', value=('uuid', 'payload'))

@public
def send(dst: str, payload: str):
    global comm
    comm += {(dst, uuid(), payload)}
