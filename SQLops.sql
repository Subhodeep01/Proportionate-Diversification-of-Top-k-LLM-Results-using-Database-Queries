show databases;
use exp;
movielistLOAD DATA LOCAL INFILE 'C:/Users/archive/title.akas.tsv/data2.csv'
INTO TABLE regions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
select * from ratings;
select * from MovieList where genres like "Comedy" limit 5;
desc MovieList;
desc ratings;
desc regions;
