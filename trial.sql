.open  
.mode box

PRAGMA foreign_keys = ON;

  
-- COMPLETLY REMOVE THE TABLE IF IT IS THERE
DROP TABLE IF EXISTS <table name>;

-- CREATE THE TABLE FRESH AND NEW (IT WILL BE EMPTY)
CREATE TABLE IF NOT EXISTS <table name>(
  id integer primary key autoincrement,
  <col1> <data type>,
  <col2> <data type> <options>
);

-- LOAD THE TABLE WITH SOME DTATA TO START OFF WITH
INSERT INTO <table name> (col1, col2, col3) VALUES (val1, val2, val3);
