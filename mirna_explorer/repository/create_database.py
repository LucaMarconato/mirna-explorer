import os
import sqlite3
import csv
import subprocess
import pandas as pd
import progressbar
import re

# delete the database, used when debugging
subprocess.call('rm database/mirna_explorer.sqlite*', shell=True)

DATA_FOLDER = '../../../mirna_target_prediction/data/'

MIRNA_ID_DICTIONARY_FILE = 'processed/mirna_id_dictionary.tsv'
MIRNA_FAMILY_INFO_FILE = 'raw/miR_Family_Info.txt'
GENE_ID_DICTIONARY_FILE = 'processed/gene_id_dictionary.tsv'
SCORED_INTERACTIONS_FILE = 'processed/scored_interactions.tsv'
SCORED_INTERACTIONS_PROCESSED_FILE = 'processed/scored_interactions_processed.tsv'
UTR_SEQUENCES_FILE = 'raw/UTR_Sequences.txt'
REQUIRED_FILES = [MIRNA_ID_DICTIONARY_FILE,
                  MIRNA_FAMILY_INFO_FILE,
                  GENE_ID_DICTIONARY_FILE,
                  SCORED_INTERACTIONS_FILE,
                  UTR_SEQUENCES_FILE]

# DB_PATH = './database/mirna_explorer.sqlite'

# for filename in REQUIRED_FILES:
#     path = DATA_FOLDER + filename
#     if not os.path.isfile(path):
#         print(f'error: file not found: "{path}", aborting')
#         exit(1)

# if os.path.isfile(DB_PATH):
#     print(f'the database is already present at {DB_PATH}, aborting')
#     exit(1)

# db_connection = sqlite3.connect(DB_PATH)
# db = db_connection.cursor()

# with open('./model/design.sql') as infile:
#     script = infile.read()
#     print('running sqlite3 script, ', end='')
#     db.executescript(script)
#     print(f'created database in {DB_PATH}')
#     db_connection.commit()


# # populate the seed_match_type table
# db.execute(('INSERT INTO seed_match_types (id, type) '
#             'VALUES(?, ?)'), (0, '8mer'))
# db.execute(('INSERT INTO seed_match_types (id, type) '
#             'VALUES(?, ?)'), (1, '7mer-m8'))
# db.execute(('INSERT INTO seed_match_types (id, type) '
#             'VALUES(?, ?)'), (2, '7mer-A1'))

# # populate the mirnas table, here we consider only the human miRNAs
# all_mirnas = pd.read_csv(DATA_FOLDER + MIRNA_FAMILY_INFO_FILE, delimiter='\t')
# # 9606 is the species id for homo sapiens
# human_mirnas = all_mirnas.loc[all_mirnas['Species_ID'] == 9606, :]

# with open(DATA_FOLDER + MIRNA_ID_DICTIONARY_FILE) as infile:
#     content = csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE)
#     header = content.__next__()
#     for row in content:
#         mirna_family = row[0]
#         mirna_family = mirna_family
#         mirna_id = int(row[1])
#         sequence = human_mirnas.loc[human_mirnas['MiRBase_ID'] ==
#                                     mirna_family.replace('hsa-mir', 'hsa-miR'),
#                                     'Mature_sequence'].values[0]
#         db.execute(('INSERT INTO mirnas (mirna_id, family, sequence) '
#                     'VALUES(?, ?, ?)'), (mirna_id, mirna_family, sequence))
#----------------------------------------------------------------------------------------------------
mirnas_dictionary = pd.read_csv(DATA_FOLDER + MIRNA_ID_DICTIONARY_FILE,
                                delimiter='\t')
print('reading scored_interactions file')
if 'scored_interactions' not in locals():
    scored_interactions = pd.read_csv(DATA_FOLDER + SCORED_INTERACTIONS_FILE,
                                      delimiter='\t')
print('done')

mirnas_dictionary['mirna_family'] = mirnas_dictionary[
    'mirna_family'].apply(lambda x: x.replace('hsa-mir', 'hsa-miR'))

# build a dict from the data frame
mirnas_dictionary = pd.Series(
    mirnas_dictionary.mirna_id_cpp.values,
    index=mirnas_dictionary.mirna_family
).to_dict()

# scored_interactions['mirna_family'] = scored_interactions[
# 'mirna_family'].apply(lambda x: mirnas_dictionary[x])

# change the names of the columns to match the ones used int the
# database schema
new_columns = scored_interactions.columns.values
new_columns[0] = 'mirna_id'
new_columns[1] = 'ensembl_id_and_version'
new_columns[2] = 'gene_name'
new_columns[3] = 'transcript_id_and_version'
scored_interactions.columns = new_columns

# split the variables ensembl_id_and_version and transcript_id_and_version into
# two separate pieces
scored_interactions['ensembl_id'] = None
scored_interactions['ensembl_version'] = None
scored_interactions['transcript_id'] = None
scored_interactions['transcript_version'] = None

print('splitting ensembl_id_and_version into ensembl_id and ensembl_version')
scored_interactions[['ensembl_id', 'ensembl_version']] = scored_interactions[
    'ensembl_id_and_version'].str.split('.', expand=True)

print(('splitting transcript_id_and_version into transcript_id '
       'and transcript_version'))
scored_interactions[['transcript_id',
                     'transcript_version']] = scored_interactions[
    'transcript_id_and_version'].str.split('.', expand=True)

scored_interactions.drop(columns=['ensembl_id_and_version',
                                  'transcript_id_and_version'], inplace=True)

genes_dictionary = pd.read_csv(DATA_FOLDER + GENE_ID_DICTIONARY_FILE,
                               delimiter='\t')
genes_dictionary.columns = ['ensembl_id', 'gene_id']

print('updating gene_id')
scored_interactions = scored_interactions.merge(genes_dictionary,
                                                on='ensembl_id',
                                                how='inner')

genes_df = scored_interactions[['gene_id', 'ensembl_id', 'ensembl_version',
                                'gene_name', 'transcript_id',
                                'transcript_version']].copy()
genes_df.drop_duplicates(keep="first", inplace=True)
# python gives a warning here: SettingWithCopyWarning:
# A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead
#
# See the caveats in the documentation:
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
genes_df['utr_sequence'] = None
# breakpoint()
# associating utr_sequences to genes
regexp = r'^[a-zA-Z0-9\.]+?\s[a-zA-Z0-9\.]+?\s[-a-zA-Z0-9\.]+?\s[0-9]+?\s[-ACGUNacgun]+$'
r = re.compile(regexp)
lines_found_per_genes = set()
print('updating utr sequences')
# breakpoint()
bar = progressbar.ProgressBar(maxval=len(genes_df),
                              widgets=[progressbar.Bar('=', '[', ']'),
                                       ' ', progressbar.Counter()])
bar.start()
i = 1
with open(DATA_FOLDER + UTR_SEQUENCES_FILE, 'r') as infile:
    header = True
    for line in infile:
        if header:
            header = False
            continue
        line = line.rstrip('\n')
        if r.match(line) is None:
            print(f"error: cannot parse the line using the regexp\n'{line}'")
            exit(1)
        else:
            split = line.split('\t')
            species_id = int(split[3])
            if species_id == 9606:
                ensembl_id_and_version = split[1]
                ensembl_split = ensembl_id_and_version.split('.')
                if len(ensembl_split) == 2:
                    ensembl_id = ensembl_split[0]
                else:
                    ensembl_id = ensembl_id_and_version
                utr_sequence = split[4].replace('-', '')
                genes_df.loc[genes_df.ensembl_id == ensembl_id, 'utr_sequence'] = utr_sequence
                if ensembl_id not in lines_found_per_genes:
                    lines_found_per_genes.add(ensembl_id)
                else:
                    print(f'error: utr_sequence already added for gene {ensembl_id}')
                    exit(1)
                # print('cancaroooo')
                bar.update(i)
                i += 1
                # breakpoint()
bar.finish()


# scored_interactions = pd.concat([
#     mirnas_dictionary.set_index('mirna_family'),
#     scored_interactions.set_index('mirna_family')
# ], axis=1, join='inner')

# db_connection.commit()
# db_connection.close()
print('finished')
