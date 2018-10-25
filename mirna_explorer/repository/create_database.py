import os
import sqlite3
import csv
import subprocess
import pandas as pd

# delete the database, used when debugging
subprocess.call('rm database/mirna_explorer.sqlite*', shell=True)

DATA_FOLDER = '../../../mirna_target_prediction/data/'

MIRNA_ID_DICTIONARY_FILE = 'processed/mirna_id_dictionary.tsv'
MIRNA_FAMILY_INFO_FILE = 'raw/miR_Family_Info.txt'
GENE_ID_DICTIONARY_FILE = 'processed/gene_id_dictionary.tsv'
SCORED_INTERACTIONS_FILE = 'processed/scored_interactions_processed.tsv'
UTR_SEQUENCES_FILE = 'raw/UTR_Sequences.txt'
REQUIRED_FILES = [MIRNA_ID_DICTIONARY_FILE,
                  MIRNA_FAMILY_INFO_FILE,
                  GENE_ID_DICTIONARY_FILE,
                  SCORED_INTERACTIONS_FILE,
                  UTR_SEQUENCES_FILE]

DB_PATH = './database/mirna_explorer.sqlite'

for filename in REQUIRED_FILES:
    path = DATA_FOLDER + filename
    if not os.path.isfile(path):
        print(f'error: file not found: "{path}", aborting')
        exit(1)

if os.path.isfile(DB_PATH):
    print(f'the database is already present at {DB_PATH}, aborting')
    exit(1)

db_connection = sqlite3.connect(DB_PATH)
db = db_connection.cursor()

with open('./model/design.sql') as infile:
    script = infile.read()
    print('running sqlite3 script, ', end='')
    db.executescript(script)
    print(f'created database in {DB_PATH}')
    db_connection.commit()


# populate the seed_match_type table
db.execute(('INSERT INTO seed_match_types (id, type) '
            'VALUES(?, ?)'), (0, '8mer'))
db.execute(('INSERT INTO seed_match_types (id, type) '
            'VALUES(?, ?)'), (1, '7mer-m8'))
db.execute(('INSERT INTO seed_match_types (id, type) '
            'VALUES(?, ?)'), (2, '7mer-A1'))

# populate the mirnas table, here we consider only the human miRNAs
all_mirnas = pd.read_csv(DATA_FOLDER + MIRNA_FAMILY_INFO_FILE, delimiter='\t')
# 9606 is the species id for homo sapiens
human_mirnas = all_mirnas.loc[all_mirnas['Species_ID'] == 9606, :]

with open(DATA_FOLDER + MIRNA_ID_DICTIONARY_FILE) as infile:
    content = csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE)
    header = content.__next__()
    for row in content:
        mirna_family = row[0]
        mirna_family = mirna_family
        mirna_id = int(row[1])
        sequence = human_mirnas.loc[human_mirnas['MiRBase_ID'] ==
                                    mirna_family.replace('hsa-mir', 'hsa-miR'),
                                    'Mature_sequence'].values[0]
        db.execute(('INSERT INTO mirnas (mirna_id, family, sequence) '
                    'VALUES(?, ?, ?)'), (mirna_id, mirna_family, sequence))

# TODO: then next step is to insert genes
        
db_connection.commit()
db_connection.close()
print('finished')
