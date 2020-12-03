from buddy import Channel, Table, View
from buddy import ADDR, uuid, init

"""
Ideally this version
is more amenable to static analysis
"""

workers = Table(key='@addr', value=('pid', 'file_uri'))

kmers = Table(key='uuid', value='seq')
result = View(query="""
                    SELECT seq, COUNT(*)
                    FROM kmers
                    GROUP BY seq
                    """)

def read_dna_file():
    global kmers
    with open(workers[ADDR].file_uri, chunks=len(workers), mode='r_char') as chunk[workers[ADDR].pid]:
        kmers += {(uuid(), chunk[i: i + 4]) for i in range(len(chunk)) if i + 4 <= len(chunk)}

# Only init can have arguments. They're assignee.
@init
def orchestrate(addresses, dna_file_uri):
    global workers
    workers += {(a, i, dna_file_uri) for i, a in enumerate(addresses)}

