import sys
import requests
import json

mesh_map_filename = 'MeSH_name_id_mapping_2018.txt'

def read_map_file(filename):
    handle = open(filename, 'r')
    mesh_map = {}
    for line in handle:
        if len(line.strip()) > 0:
            mesh, index = line.strip().split("=")
            mesh = mesh.replace(" ", "_").replace(",","")
            mesh_map[mesh] = index
    handle.close()
    return mesh_map

if __name__ == "__main__":
    mesh_map = read_map_file(mesh_map_filename)
    outfile = open("/mnt/nfs/scratch1/lingeman/bioasq_train/mesh_tokens.txt", 'w')
    tokens = mesh_map.keys()
    for t in sorted(tokens):
        outfile.write(t + "\n")
    outfile.close()
