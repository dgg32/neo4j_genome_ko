import sys, re, os, json
import pyphy

rx_entry = re.compile(r'ENTRY\s+(\w+)')
rx_name = re.compile(r'NAME\s+(.+)')
rx_gene = re.compile(r'\s+(\w+):\s+(.+)')

top_folder = sys.argv[1]
list_file = sys.argv[2]

short_taxid = {}

for line in open(list_file):
    fields = line.strip().split("\t")

    short_taxid[fields[0].lower()] = fields[1]


def parse_gene(line):

    line = line.replace("GENES", " ")

    match_gene = rx_gene.match(line)

    if match_gene:
        genome = match_gene.group(1)
        genes = match_gene.group(2)
        amount_genes = len(genes.split(" "))

        if genome.lower() in short_taxid:
    
            return [short_taxid[genome.lower()], amount_genes]
        else:
            return []
        
#print (",".join(["taxid", "genome_size", "name"]))
with open("kegg.csv", "w") as output:
    #o"taxid", "name", "label"
    output.write(",".join(["ko_id", "name", "label"]) + "\n")

with open("has_kegg.csv", "w") as output:
    output.write(",".join(["taxid", "ko_id"]) + "\n")

for (head, dirs, files) in os.walk(top_folder):
    for file in files:
        current_file_path = os.path.abspath(os.path.dirname(os.path.join(head, file)))
        with_name = current_file_path + "/"+ file

        entry = ""
        name = ""
        genomes = {}

        is_gene = False

        for line in open(with_name, 'r'):
            if line.startswith("NAME"):
                search_name = rx_name.search(line)

                if search_name:
                    name = search_name.group(1).replace('"', "'")

            
            if line.startswith("GENES"):
                is_gene = True

                group = parse_gene(line)

                if len(group) >0 :
                    genomes[group[0]] = group[1]


            elif is_gene == True:
                if line.startswith(" "):
                    
                    group = parse_gene(line)

                    if len(group) > 0:
                        genomes[group[0]] = group[1]
                else:
                    is_gene = False


            search_entry = rx_entry.search(line)

            if search_entry:
                entry = search_entry.group(1)

        #print (entry, definition, genomes)

        #["~id", "name:String", "taxid:Int", "~label"]
        with open("kegg.csv", "a+") as output:
            #o"taxid", "name", "label"
            output.write(",".join([entry, f'"{name}"', "ko"]) + "\n")


        #["~id", "~from", "~to", "~label"]

        with open("has_kegg.csv", "a+") as output:
            for genome in genomes:
            #    output.write(f"{genome},{entry},{genomes[genome]}\n")
                output.write(f"{genome},{entry}\n")