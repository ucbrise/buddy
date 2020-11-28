from buddy import Channel, Table
from buddy import init, utils

workers = Table(key='@addr', value=('pid', 'file_uri'))

kmers = Table(key='uuid', value='seq')
result = kmers.view().groupby('seq').count()
   
def read_dna_file():
    _, pid, file_uri = workers[utils.MY_ADDR]
    file = utils.open_chunk(file_uri, pid, len(workers), mode='r_char')
    kmers += {(utils.uuid(), file[i: i+4]) for i in range(len(file)) if i+4 <= len(file)}
    
@init
def orchestrate(addresses, dna_file_uri):
    global workerks
    workers += {(a, i, dna_file_uri) for i, a in enumerate(addresses)}