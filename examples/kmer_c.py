from buddy import Channel, Table, View
from buddy import uuid, init

"""
Ideally this version
is more amenable to static analysis
"""

worker = Channel(key='@addr', value=('file_uri', 'num_workers'))

kmers = Table(key='uuid', value='seq')
result = View(query="""
                    SELECT seq, COUNT(*)
                    FROM kmers
                    GROUP BY seq
                    """)

def read_dna_file():
    global kmers
    with open(worker.file_uri, chunks=worker.num_workers, addr=worker.addr, mode='r_char') as chunk:
        """
        chunk = Channel(key='@addr', value: Character Stream for 1/n th of the file)
        chunk[i:i+4] is monotonic (no point of order despite seq type) as long as we receive packets of 4 characters 
        each... then each packet may be reordered
        """
        kmers += {(uuid(), chunk[i: i+4]) for i, _ in enumerate(chunk)}

# Only init can have arguments. They're assignee.
@init
def orchestrate(addresses: 'Set[str]', dna_file_uri: str):
    global worker
    worker += {(a, dna_file_uri, len(addresses)) for a in addresses}

