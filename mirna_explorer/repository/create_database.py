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

# populate the mirnas table
all_mirnas = pd.read_csv(DATA_FOLDER + MIRNA_FAMILY_INFO_FILE, delimiter='\t')
human_mirnas = all_mirnas.loc[df['Species_ID'] == 9606, :]
# The columns "miR_family" specifies the human-readable name for the miRNA.
# For example, a value for miR_family is "let-7".
# Sometimes the value of miR_family contains one or more slashes, to identity
# that the row in the dataframe refers to more than one miRNAs
# An example is let-7/98, which stands for let-7 and let-98
# In few cases the value can be something like let-7-3p/miR-3596d/98-3p, which
# stands for let-7-3p, miR-3596d, miR-98-3p
# In the lines of code I remove these rows by replacing them with the
# equivalent explicit rows
human_mirnas_expanded <---------- TODO CONTINUE CODING HERE

with open(DATA_FOLDER + MIRNA_ID_DICTIONARY_FILE) as infile:
    content = csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE)
    header = content.__next__()
    for row in content:
        mirna_family = row[0]
        mirna_id = int(row[1])
        sequence = 'dummy'
        db.execute(('INSERT INTO mirnas (mirna_id, family, sequence) '
                    'VALUES(?, ?, ?)'), (mirna_id, mirna_family, sequence))

db_connection.commit()
db_connection.close()
print('finished')
