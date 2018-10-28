-- Creator:       MySQL Workbench 8.0.12/ExportSQLite Plugin 0.1.0
-- Author:        macpoule
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2018-10-16 22:28
-- Created:       2018-10-16 00:43
PRAGMA foreign_keys = OFF;

-- Schema: mydb
-- ATTACH "db.sdb" AS "mydb";
BEGIN;
CREATE TABLE "genes"(
  "gene_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK("gene_id">=0),-- This is the id which is used inside the C++ program in mirna_target_prediction
  "ensembl_id" VARCHAR(20) NOT NULL,
--   An example of ENSEMBL id is ENSG00000139618, usually it is also specified a version, like ENSG00000139618.10.
--   This variable only contains the id, so in this case it would be ENSG00000139618
  "ensembl_version" VARCHAR(45),
--   An example of ENSEMBL id is ENSG00000139618, usually it is also specified a version, like in ENSG00000139618.10.
--   This variable only contains the version number, so in this case it would be 10
  "transcript_id" VARCHAR(45) NOT NULL,
--   The same gene can be spliced and in different ways so it can give rise to different RNAs.
--   For this reason usually there are different transcripts associated to a gene.
--   An example of transcript id ENST00000380152. Usually it is also specified a version, like in ENST00000380152.7.
--   This variable only contains the id, so in this case it would be ENST00000380152.
  "transcript_version" INTEGER CHECK("transcript_version">=0),
--   The same gene can be spliced and in different ways so it can give rise to different RNAs.
--   For this reason usually there are different transcripts associated to a gene.
--   An example of transcript id ENST00000380152. Usually it is also specified a version, like in ENST00000380152.7.
--   This variable only contains the version number, so in this case it would be 7.
  "name" VARCHAR(20) NOT NULL,
--   The human readable name used for the gene. 
--   Warning: I found cases in which the same human readable name was the same for different ensebl_id or the same transcript_id.
  "utr_sequence" VARCHAR(15000) NOT NULL,-- A sequence of ACGU letters.
  CONSTRAINT "rowid_UNIQUE"
    UNIQUE("gene_id"),
  CONSTRAINT "ensembl_id_UNIQUE"
    UNIQUE("ensembl_id"),
  CONSTRAINT "transcript_id_UNIQUE"
    UNIQUE("transcript_id")
);
CREATE TABLE "mirnas"(
  "mirna_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL CHECK("mirna_id">=0),-- mirna_Id is used in the C++ code
  "family" VARCHAR(20) NOT NULL,-- human readable name
  "sequence" VARCHAR(40),-- Sequence of ACGU characters.
  CONSTRAINT "rowid_UNIQUE"
    UNIQUE("mirna_id")
);
CREATE TABLE "seed_match_types"(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "type" VARCHAR(10) NOT NULL
--   This value can 
--   “8mer”
--   “7mer_m8”
--   “7mer_a1”
--   
--   In the C++ code the above values corresponds to an enum with value 0, 1, 2
);
CREATE TABLE "clusters"(
  "cluster_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL-- This value is not used in the C++ code since a pointer to the object is enough to specify it.
);
CREATE TABLE "scored_interactions"(
  "mirna_id" INTEGER NOT NULL CHECK("mirna_id">=0),
  "gene_id" INTEGER NOT NULL CHECK("gene_id">=0),
  "utr_start" INTEGER NOT NULL CHECK("utr_start">=0),
  "seed_match_type" INTEGER NOT NULL CHECK("seed_match_type">=0),
  "context_score" INTEGER NOT NULL,
  "weighted_context_score" INTEGER NOT NULL,
  "conserved" INTEGER NOT NULL,
  PRIMARY KEY("mirna_id","gene_id","utr_start"),
  CONSTRAINT "mirna_id"
    FOREIGN KEY("mirna_id")
    REFERENCES "mirnas"("mirna_id"),
  CONSTRAINT "gene_id"
    FOREIGN KEY("gene_id")
    REFERENCES "genes"("gene_id")
);
CREATE INDEX "scored_interactions.gene_id_idx" ON "scored_interactions" ("gene_id");
CREATE TABLE "sites"(
  "gene_id" INTEGER NOT NULL CHECK("gene_id">=0),
  "utr_start" INTEGER NOT NULL CHECK("utr_start">=0),
  "seed_match_type" INTEGER NOT NULL CHECK("seed_match_type">=0),
  "clusters_cluster_id" INTEGER NOT NULL,
  PRIMARY KEY("gene_id","utr_start","seed_match_type","clusters_cluster_id"),
  CONSTRAINT "gene_id"
    FOREIGN KEY("gene_id")
    REFERENCES "genes"("gene_id"),
  CONSTRAINT "seed_match_type"
    FOREIGN KEY("seed_match_type")
    REFERENCES "seed_match_types"("id"),
  CONSTRAINT "fk_sites_clusters1"
    FOREIGN KEY("clusters_cluster_id")
    REFERENCES "clusters"("cluster_id")
);
CREATE INDEX "sites.seed_match_type_idx" ON "sites" ("seed_match_type");
CREATE INDEX "sites.fk_sites_clusters1_idx" ON "sites" ("clusters_cluster_id");
COMMIT;
