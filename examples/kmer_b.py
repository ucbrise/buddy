import pysqldf
from buddy import Channel, Table, LocalTable, Index
from buddy import garbage_collect, periodic, tick
from buddy import init, utils


workers = Table(key='@addr', value=('pid', 'dna_base', 'file_uri'))
base_to_addr = Index(workers, key='dna_base', value='addr', fetch_next='tuple',
                fetch_mode='coin_flip')


kmer_stream = Channel(key='uuid' value=('seq', '@addr', 'sender'))
ack_chan = Channel(key='@dst', value='uuid')

kmer_buffer = LocalTable(key='uuid' value=('seq', 'addr', 'sender'))
result = Table(key='seq', value='num_seqs')

def count():
    global result, ack_chan
    ack_chan += {(t.sender, t.uuid) for t in kmer_stream}
    result += pysqldf(
        """
        SELECT seq, COUNT(uuid)
        FROM kmer_stream
        GROUP BY seq
        """
    )
    

def read_dna_file():
    global kmer_buffer, kmer_stream
    _, pid, dna_base, file_uri = workers[utils.MY_ADDR]
    file = utils.open_chunk(file_uri, pid, len(workers), mode='r_char')

    kmer_buffer += {(utils.uuid(), file[i: i+4], base_to_addr[file[i]].next(), utils.MY_ADDR) 
                for i in range(len(file)) if i+4 <= len(file)}
    kmer_stream += kmer_buffer
    
@init
def orchestrate(addresses, dna_file_uri):
    global workerks
    while len(workers) < len(addresses):
        for i,a in enumerate(addresses):
            if  i % 4 == 0:
                workers += {(a, i, 'A', dna_file_uri)}
            elif i % 4 == 1:
                workers += {(a, i, 'T', dna_file_uri)}
            elif i % 4 == 2:
                workers += {(a, i, 'C', dna_file_uri)}
            else:
                workers += {(a, i, 'G', dna_file_uri)}
    
                
@garbage_collect
def forget():
    global kmer_buffer
    kmer_buffer = pysqldf(
        """
        SELECT *
        FROM kmer_buffer
        WHERE uuid NOT IN 
            (SELECT uuid FROM ack_chan)
        """
    )

@periodic(s=10)
def timer_retry():
    global kmer_stream
    kmer_stream += kmer_buffer