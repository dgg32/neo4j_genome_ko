
# Analyzing Genomes in a Graph Database
This repository hosts the code and the data for the post [Analyzing Genomes in a Graph Database](https://dgg32.medium.com/analyzing-genomes-in-a-graph-database-27a45faa0ae8).

## Prerequisites:

If you want to prepare the data yourself, you need the [pyphy](https://github.com/dgg32/pyphy) library.

First, clone the [pyphy](https://github.com/dgg32/pyphy) repo, and prepare both the library and the data following the instructions there.



## Scripts
1. First, **download_kegg_various_databases.py** download data from KEGG via its API. To download the genomes, run:

    python download_kegg_various_databases.py genome [genome_output_folder]

  
2. Then use **download_kegg_various_databases.py** again to download the KO:

    python download_kegg_various_databases.py ko  [ko_output_folder]
    
Sometimes these two commands will miss some files because of the network connection. Rerun the command. It will check which files are already downloaded and then it will only download those missing files. 
      
3. Use **genome_parser.py** to process the genome data:
  

    python genome_parser.py [genome_folder] [target_taxonomic_rank] [target_taxonomic_name]
     
+ where target_taxonomic_rank and target_taxonomic_name are the taxonomic group you want to analyze. For the article, I use "phylum" and "Proteobacteria".
+ It outputs a mapping.csv file, which is needed for the next step.
 
4. Use **kegg_parser.py** to process the KO data: 
    
    python kegg_parser.py [ko_output_folder] [path_to_mapping.csv]

After finishing these steps, four csv files needed for Neo4j are produced, connections.csv, has_kegg.csv, kegg.csv, taxon.csv.

I have also attached mine in the repo.

## Authors

* **Sixing Huang** - *Concept and Coding*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

