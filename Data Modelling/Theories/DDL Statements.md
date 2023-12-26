# `Data Definition Language` 

(DDL) statements are an integral part of data modelling; 

you will use them extensively to create the structure of several entities in your database.

<br>

      Using DDL statements, you can specify the following:

- The table structure 
- The different columns that belong to a table
- The data type of each of those columns
- The relationship between multiple entities

----------------

    The most important DDL statements are as follows:

- `CREATE`: To create the table structure
- `ALTER`: To modify the table structure
- `DROP`: To remove the table structure

----------------

## Creating a Table

You are asked to compile data and analyze India's performance in the 2019 Cricket World Cup. 

The first step you would perform is creating a table having some columns with the appropriate data types. 

Write a query to create a table named `India` having columns with the following `data types`:

      matches_played - INT
      matches_won - INT
      matches_lost - INT
      net_run_rate - DECIMAL(4,3)
      points - INT

<br>

```sql
CREATE TABLE India
(
  matches_played INT,
  matches_won INT,
  matches_lost INT,
  net_run_rate DECIMAL(4,3),
  points INT
);
```

`Note`: The net run rate has the format: DECIMAL(4,3). 

So, a value for the same can be 1.234. 

In DECIMAL(4,3), 4 is the total number of digits, while 3 is the total number of digits after the decimal point. 

This is the SQL standard specification.
