import sys, re, os, json
from pyphy import pyphy

rx_short = re.compile(r'ORG_CODE\s+(\S+)')
rx_name = re.compile(r'NAME\s+(.+)')
rx_taxonomy = re.compile(r'TAXONOMY    TAX:(\d+)')

top_folder = sys.argv[1]
filter_rank = sys.argv[2]
filter_taxon = sys.argv[3]

existing_mapping = set()

if os.path.isfile("mapping.tsv"):
    with open("mapping.tsv", "r") as input:
        for line in input.readlines():
            line = line.strip()

            existing_mapping.add(line)


short_taxid = {}

taxid_taxon = {}

parent_son = set()

desired_rank = ["superkingdom", "phylum", "class", "order", "family", "genus", "species", "genome"]

#print (",".join(["taxid", "genome_size", "name"]))

with open("taxon.csv", "w") as output:
    output.write(",".join(["taxid", "name", "rank"]) + "\n")

with open("connections.csv", "w") as output:
    output.write(",".join(["from", "to"]) + "\n")
            

for (head, dirs, files) in os.walk(top_folder):
    for file in files:
        current_file_path = os.path.abspath(os.path.dirname(os.path.join(head, file)))
        with_name = os.path.join(current_file_path, file)

        short_cut = ""
        name = ""
        taxid = -1

        for line in open(with_name, 'r'):


            
            if line.startswith("NAME"):

                search_name = rx_name.search(line)

                if search_name:
                    name = search_name.group(1)

            if line.startswith("ORG_CODE"):
                search_short = rx_short.search(line)

                if search_short:
                    short_cut = search_short.group(1)
            
            if line.startswith("TAXONOMY"):
                search_taxonomy = rx_taxonomy.search(line)

                if search_taxonomy:
                    taxid = int(search_taxonomy.group(1))

        #print (file)

        if taxid != -1:
            dict_path = pyphy.getDictPathByTaxid(taxid)

            dict_path["genome"] = taxid
            quartett = [""] * 2

            #print (dict_path)

            if filter_rank in dict_path and pyphy.getNameByTaxid(dict_path[filter_rank]) == filter_taxon:

                for rank in desired_rank:
                    if rank in dict_path:

                        name = pyphy.getNameByTaxid(dict_path[rank])

                        if rank == "superkingdom":


                                quartett[0] = dict_path[rank]

                                if dict_path[rank] not in taxid_taxon:
                                    taxid_taxon[dict_path[rank]] = [name, rank]
                        else:

                            quartett[1] = dict_path[rank]

                            if quartett[0] != quartett[1]:
                                parent_son.add(tuple(quartett))

                                if dict_path[rank] not in taxid_taxon:
                                    taxid_taxon[dict_path[rank]] = [name, rank]

                                quartett[0] = quartett[1]
                
                mapping = f"{short_cut}\t{taxid}"

                if mapping not in existing_mapping:
                    with open("mapping.tsv", "a+") as output:

                        output.write(f"{mapping}\n")

#print (taxid_taxon)

#print (parent_son)

for taxid in taxid_taxon:
    with open("taxon.csv", "a") as output:
        output.write(",".join([f"{taxid}", f'"{taxid_taxon[taxid][0]}"', f'"{taxid_taxon[taxid][1]}"']) + "\n")

for parent in parent_son:
    with open("connections.csv", "a") as output:
        #["~id", "~from", "~to", "~label"]
        output.write(",".join([f"{parent[0]}", f"{parent[1]}"]) + "\n")