from buddy import Channel, Table, View
from buddy import uuid, init

"""
Ideally this version
is more amenable to static analysis
"""

worker = Channel(key='@addr', value='file_uri')

kmers = Table(key='uuid', value='seq')
result = View(query="""
                    SELECT seq, COUNT(*)
                    FROM kmers
                    GROUP BY seq
                    """)

"""
A stream is an Iterator: implements open, next, close
By defining it as a func arg, we ensure that it is open by first statement
and closed on function end.
"""
def read_dna_file(kmer_stream=open(worker.file_uri, req_id=uuid(),
                                   addr=worker.addr, mode='char[4]')):
    global kmers
    kmers += {(uuid(), kmer) for kmer in kmer_stream}


# Only init can have arguments. They're assignee.
@init
def register_worker(address: 'str', dna_file_uri: str):
    global worker
    worker += {(address, dna_file_uri)}
