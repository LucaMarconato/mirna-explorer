## Creating the database - Instructions

The database structure is described in the file `./model/design.mwb` (see also `./model/design.png`).
The create is script is `./model/design.sql`. The create script is just a minor modification of the script generated from the `./model/design.mwb` since the line `ATTACH "db.sdb" AS "mydb"` has been removed and also all the references to the schema `"mydb"`.
So, if you modify the database structure and regenerate the create script, you may need to apply these modifications.

The script `./create_database.py` executes `.model/design.sql` creating a database under `./database/db.sqlite`. Then, the script populates the database with the data. 
The script requires the data to be available, so before creating the database it checks if the data files exists.
It is recommended to clone the repository (mirna\_target\_prediction)[https://github.com/LucaMarconato/mirna_target_prediction] in the same folder in which this repository has been cloned, so that `mirna_explorer` will use the raw and processed data used in `mirna_target_prediction`.





