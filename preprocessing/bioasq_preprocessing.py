import sys
import zipfile
import json
import naya
import os
from genia_tokenizer import *

WORK_DIR = "/mnt/nfs/scratch1/lingeman/"
ALL_MESH_FILENAME = WORK_DIR + "mesh_tokens.txt"

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

def load_bioasq_test(filename):
    handle = open(filename, 'r')
    test_data = json.load(handle)
    handle.close()
    return test_data

def parse_bioasq_test(test_data):
    entries = {}
    for entry in test_data:
        title = entry["title"]
        abstract = entry["abstractText"]
        journal = entry["journal"]
        pmid = entry["pmid"]
        text = " ".join(tokenize(title)) + " <EOT> " + " ".join(tokenize(abstract))
        entries[pmid] = text
    return entries

def parse_bioasq_dev(directory, output_filename):
    entries = {}
    test_data = "test_data"
    test_results = "test_results"
    mesh_map = read_map_file(mesh_map_filename)
    mesh_map_rev = {v: k for k,v in mesh_map.items()}
    output_text_handle = open(output_filename + ".text", 'w')
    output_mesh_handle = open(output_filename + ".mesh", 'w')
    output_pmid_handle = open(output_filename + ".pmid", 'w')
    for f in os.listdir(directory + "/" + test_data):
        if f.endswith(".json"):
            data = load_bioasq_test(directory + "/" + test_data + "/" + f)
            for d in data:
                entries[d['pmid']] = d
                text = " ".join(tokenize(d['title'])) + " <EOT> " + " ".join(tokenize(d['abstractText']))
                entries[d['pmid']]['text'] = text
    for f in os.listdir(directory + "/" + test_results):
        if f.endswith(".json") and "MTIDEF" in f:
            data = load_bioasq_test(directory + "/" + test_results + "/" + f)
            for d in data["documents"]:
                entries[d['pmid']]['labels'] = d['labels']
    for pmid, doc in entries.items():
        try:
            mesh_terms = doc['labels']
            mesh_terms = ["_".join(t.replace(",", "").split(" ")) for t in mesh_terms]
            mesh_terms.sort()
            mesh_terms = " ".join(mesh_terms)
            output_text_handle.write(doc['text'] + "\n")
            output_pmid_handle.write(str(pmid) + "\n")
            output_mesh_handle.write(mesh_terms + "\n")
        except:
            print("ERROR: no labels for", pmid)
    output_text_handle.close()
    output_pmid_handle.close()
    output_mesh_handle.close()



def parse_bioasq_train(train_filename, output_filename):
    # Giant file, so we need to stream it
    handle = open(train_filename, 'r')
    handle.readline() # Burn the first line, we dont want it
    output_text_handle = open(output_filename + ".text", 'w')
    output_mesh_handle = open(output_filename + ".mesh", 'w')
    output_pmid_handle = open(output_filename + ".pmid", 'w')
    for line in handle:
        entry = json.loads(line.strip()[:-1]) # Remove trailing comma
        title = entry["title"]
        abstract = entry["abstractText"]
        journal = entry["journal"]
        pmid = entry["pmid"]
        mesh_terms = entry["meshMajor"]
        year = entry["year"]
        mesh_terms = ["_".join(t.replace(",", "").split(" ")) for t in mesh_terms]
        mesh_terms.sort()
        mesh_terms = " ".join(mesh_terms)
        text = " ".join(tokenize(str(title))) + " <EOT> " + " ".join(tokenize(str(abstract)))

        output_text_handle.write(text + "\n")
        output_mesh_handle.write(mesh_terms + "\n")
        output_pmid_handle.write(str(pmid) + "\n")
    output_text_handle.close()
    output_pmid_handle.close()
    output_mesh_handle.close()
    handle.close()


if __name__ == "__main__":
    if sys.argv[1] == "test":
        filename = sys.argv[2]
        test_data = load_bioasq_test(filename)
        entries = parse_bioasq_test(test_data)
        output_text_file = open(filename + ".parsed", 'w')
        output_pmid_file = open(filename + ".pmid", 'w')
        for pmid, text in entries.items():
            output_text_file.write(text + "\n")
            output_pmid_file.write(str(pmid) + "\n")
        output_text_file.close()
        output_pmid_file.close()
    if sys.argv[1] == "train":
        filename = sys.argv[2]
        output_filename = filename # Will have extensions added
        parse_bioasq_train(filename, output_filename)
    if sys.argv[1] == "dev":
        directory = sys.argv[2]
        output_filename = "/mnt/nfs/scratch1/lingeman/bioasq_train/dev/bioasq_dev"
        parse_bioasq_dev(directory, output_filename)

