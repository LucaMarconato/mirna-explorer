import os
import sqlite3

DATA_FOLDER = '../../../mirna_target_prediction/data/'
REQUIRED_FILES = ['raw/UTR_Sequences.txt',
                  'processed/mirna_id_dictionary.tsv',
                  'processed/gene_id_dictionary.tsv',
                  'processed/scored_interactions_processed.tsv']
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

db_connection.close()

print('finished')
