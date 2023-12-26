# `Data Manipulation Language`

(DML) statements are used to modify the contents of a table instead of its structure.

<br>

    The most important DML statements are as follows:

- `INSERT`: To insert records into a table
- `UPDATE`: To update the existing records of a table
- `DELETE`: To delete records from a table

-----------------

    Note the difference between the DROP and DELETE statements. 

While `DROP` is used to remove the contents as well as the metadata of a table, 

`DELETE` removes only the contents of the table. 

DML statements operate only on the contents of a table and not on its structure.

-----------------

- DDL statements are used to create, alter and drop tables.
- DELETE is the DML statement used for this operation.
- INSERT is the DML statement used for this operation.
- RENAME is the DDL statement used for this operation.

-------------------

## Inserting Values

Suppose you have an empty table named `wrestlers` having the following columns:

    Name
    Wrestler_Rank
    Height
    Weight
    Age

Write a query to add the following values to this table:

- (Undertaker, 1, 208, 136, 54)
- (Kane, 2, 213, 147, 52)

```sql
INSERT INTO wrestlers
  (name, wrestler_rank, height, weight, age)
VALUES
  ('Undertaker', 1, 208, 136, 54),
  ('Kane', 2, 213, 147, 52);
```
