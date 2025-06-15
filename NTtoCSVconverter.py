from rdflib import Graph
import csv

g = Graph()
# the RDF-N triples {.nt extension} file that contains the data 
g.parse("", format="nt")  

with open("output.csv", "w", newline='', encoding="utf-8") as out:
    writer = csv.writer(out)
    
    # Write the header row
    # These are the columns for the CSV file
    # You can change the header names as per your requirements
    writer.writerow(["Subject", "Predicate", "Object"]) 
    for s, p, o in g:
        writer.writerow([s, p, o])
