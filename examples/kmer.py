from buddy import Channel, Table, View
from buddy import uuid, init

worker = Channel(key='@addr', value='file_uri')

kmers = Table(key='uuid', value='seq', crdt='g-set')
result = View(query="""
                    SELECT seq, COUNT(*)
                    FROM kmers
                    GROUP BY seq
                    """)

def read_dna_file(kmer_stream=open(worker.file_uri, req_id=uuid(),
                                   addr=worker.addr, mode='char[4]')):
    global kmers
    kmers += {(uuid(), kmer) for kmer in kmer_stream}

@init
def register_worker(address: 'str', dna_file_uri: str):
    global worker
    worker += {(address, dna_file_uri)}
