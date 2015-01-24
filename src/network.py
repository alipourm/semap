import json
import networkx as nx


def get_authors(json_file_name):
  data = json.load(open(json_file_name))
  papers = data['papers']
  authors = set()
  for p in papers:
    for a in p['authors']:
      authors.add(a)
  return authors


def get dois(json_file):
    
