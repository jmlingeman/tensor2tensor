import sys
import requests
import json

mesh_map_filename = 'MeSH_name_id_mapping_2018.txt'

submission = {
        "username": "jmlingeman",
        "password": open("password.txt", 'r').readline().strip(), 
        "system": "UMass-T2T",
        "documents": []
        }

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

def parse_results(pmid_filename, infer_filename, submission, mesh_map):
    pmid_handle = open(pmid_filename)
    infer_handle = open(infer_filename)
    for pmid, infer in zip(pmid_handle, infer_handle):
        pmid = int(pmid)
        infer = infer.strip().split(" ")
        inferred_indexes = set()
        for x in infer:
            if x in mesh_map:
                inferred_indexes.add(mesh_map[x])
        doc = {"pmid": pmid, "labels": sorted(list(inferred_indexes))}
        submission['documents'].append(doc)
    pmid_handle.close()
    infer_handle.close()
    return submission

def submit(test_num, submission):
    url='http://participants-area.bioasq.org/tests/uploadResults/{}/'.format(test_num)
    r=requests.post(url, data=json.dumps(submission))
    print(r.text)
    print(r.status_code)

if __name__ == "__main__":
    pmid_filename = sys.argv[2]
    infer_filename = sys.argv[3]
    test_num = sys.argv[1]
    mesh_map = read_map_file(mesh_map_filename)
    submission = parse_results(pmid_filename, infer_filename, submission, mesh_map)
    submit(test_num, submission)
