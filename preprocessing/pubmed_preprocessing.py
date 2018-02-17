import sys
import os
from collections import defaultdict
from genia_tokenizer import *

TOPK=100000
WORK_DIR = "/data/tmp/pubmed_xml/"
RAW_FILENAME = WORK_DIR + "pubmed_output.txt"
#RAW_FILENAME = WORK_DIR + "pubmed_output.txt.debug"
CLEANED_FILENAME = WORK_DIR + "pubmed_cleaned.txt"
META_FILENAME = WORK_DIR + "pubmed_meta.txt"
MESH_FILENAME = WORK_DIR + "pubmed_mesh.txt"
TOKENS_FILENAME = WORK_DIR + "pubmed_top{}k.txt".format(TOPK)
ALL_MESH_FILENAME = WORK_DIR + "mesh_tokens.txt"
MINYEAR = 0

def clean_data(infile, outfile, mesh_outfile, meta_outfile, minyear):
   # Remove lines with no abstract, title, or mesh terms
   # Remove lines below minyear
   # Convert tags to single tokens
   # Alphabetical output tags, space sep
   count = 0
   outfile = open(outfile, 'w')
   infile = open(infile, 'r')
   mesh_outfile = open(mesh_outfile, 'w')
   meta_outfile = open(meta_outfile, 'w')
   for line in infile:
      if count % 100000 == 0:
         print(count)
      line = line.split("\t")
      try:
         pmid, year, title, abstract, mesh_terms, mesh_ids = line
         count += 1
         if len(title) == 0 or len(abstract) == 0 or len(year) == 0 or len(mesh_terms) == 0:
            continue
         if int(year) < minyear:
            continue

         mesh_terms = ["_".join(t.replace(",", "").split(" ")) for t in mesh_terms.split("|")]
         mesh_terms.sort()
         mesh_terms = " ".join(mesh_terms)

         text = " ".join(tokenize(title)) + " <EOT> " + " ".join(tokenize(abstract))
         outfile.write(text + "\n")
         meta_outfile.write("\t".join([pmid, year]) + "\n")
         mesh_outfile.write(mesh_terms + "\n")
         #outstr = "\t".join([year, text, mesh_terms])
         #outfile.write(outstr + "\n")
      except:
         print("ERROR: Could not read line", line)
         print(line.split("\t"))

   mesh_outfile.close()
   outfile.close()
   infile.close()

def topk_vocab(cleaned_infile, mesh_infile, outfile, mesh_outfile, topk=10000):
   cleaned_infile = open(cleaned_infile, 'r')
   mesh_infile = open(mesh_infile, 'r')
   outfile = open(outfile, 'w')
   mesh_outfile = open(mesh_outfile, 'w')
   reserved_tokens = [("<pad>", -1), ("<EOS>", -1), ("<UNK>", -1), ("<EOT>", -1)]
   word_count = defaultdict(int)
   all_mesh_terms = set()
   for line, mesh_terms in zip(cleaned_infile, mesh_infile):
      text = line.strip()
      mesh_terms = mesh_terms.strip().split(" ")
      all_mesh_terms.update(mesh_terms)
      tokens = tokenize(text)
      for w in tokens:
         if w != "<EOT>":
            word_count[w] += 1
   topk_tokens = reserved_tokens + sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:topk - len(reserved_tokens)]
   for w in topk_tokens:
      outfile.write(w[0] + "\n")
   for t in sorted(list(all_mesh_terms)):
      mesh_outfile.write(t + "\n")
   outfile.close()
   mesh_outfile.close()
   cleaned_infile.close()
   mesh_infile.close()

clean_data(RAW_FILENAME, CLEANED_FILENAME, MESH_FILENAME, META_FILENAME, MINYEAR)
topk_vocab(CLEANED_FILENAME, MESH_FILENAME, TOKENS_FILENAME, ALL_MESH_FILENAME, topk=TOPK)
