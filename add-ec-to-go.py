import os

import argparse
import requests
from Bio.KEGG import Enzyme


ec2go = {}
go2label = {}

def main():

    parser = argparse.ArgumentParser(description='add-ec-to-go'
                                                 'Helper utils for EC',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input', type=str, default='gene_ontology_write.obo', required=False,
                        help='Input metadata file')
    parser.add_argument('files',nargs='*')

    args = parser.parse_args()
    extract_ecmap_from_go(args.input)
    for id in args.files:
        convert(id)
    
def extract_ecmap_from_go(file):    
    fh = open(file)
    id = ''
    s = {}
    for line in fh:
        line = line.strip()
        tv = line.split(":",1)
        if len(tv) > 1:
            [tag,val] = tv
            val = val.strip(" ")
            if tag == 'id':
                [id] = val.split(" ")
            elif tag == 'name':
                go2label[id] = val
            elif tag == 'xref':
                xrefstr = val.split(" ",1)
                [db,local] = xrefstr[0].split(":",1)
                if db == 'EC':
                    ec2go[local] = id
    fh.close()
    

def convert(id):
    """Fetches an EC ID from the KEGG REST API, parses it, and writes a GO record."""

    # this is a dumb way of doing it, too much of a python noob to figure a better way
    txt = fetch(id)
    fn = "target/"+id+".kml"
    fh = open(fn, "w")
    fh.write(str(txt))
    fh.close()
    fh = open(fn)

    records = Enzyme.parse(fh)
    n = 0
    for record in records:
        write_obo(record)
        n=n+1
    if n==0:
        print("FAIL")
    fh.close()
    
def fetch(id):
    url = "http://rest.kegg.jp/get/"+id
    resp = requests.get(url, stream=False)
    return resp.text

def write_obo(record):
    entry = record.entry
    parts = entry.split(".")
    lastpart = parts.pop()
    parent_entry = ".".join(parts)
    names = record.name
    name = names[0]
    syns = names[1:]
    print("[Term]")
    print("id: ")
    print('name: %s activity' % name)
    print('def: "Catalysis of the reaction: %s" [EC:%s]' % (record.reaction[0], entry))
    for s in syns:
        print('synonym: "%s" EXACT [EC:%s]' % (s, entry))
    if parent_entry in ec2go:
        pid = ec2go[parent_entry]
        pname = go2label[pid]
        print('is_a: %s ! %s' % (pid, pname) )
    else:
        print("NO SUCH PARENT: EC:%s" % parent_entry)
    print("")


if __name__ == "__main__":
    main()

