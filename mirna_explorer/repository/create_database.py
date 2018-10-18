#!/usr/bin/env python3

import os
import sqlite3

data_folder = "../../../mirna_target_prediction/data/"

required_files = ["raw/UTR_Sequences.txt",
				  "processed/mirna_id_dictionary.tsv",
				  "processed/gene_id_dictionary.tsv",
				  "processed/scored_interactions_processed.tsv"]

for filename in required_files:
	path = data_folder + filename
	if not os.path.isfile(path):
		print(f'error: file not found: \'{path}\', aborting')
		exit(1)

db_path = 'database/db.sqlite'

if os.path.isfile(db_path):
	print(f'the database is already present at {db_path}, aborting')
	exit(1)
		
db_connection = sqlite3.connect('database/db.sqlite')
db = db_connection.cursor()

with open('./model/design.sql', 'r') as infile:
	script = infile.read()
	print('running sqlite3 script, ', end = '')
	db.executescript(script)
	print('created database in ./database/db.sqlite')
	db_connection.commit()

db_connection.close()

print('finished')
