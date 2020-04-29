
tables schemas and columns, oh my
---------------------------------


conceptual data model -> logical data model -> actual ddl model


### Relational Database 
use for:
- ease of use - sql
- joins
- aggregations
- smaller data
- easier to change
- flexible for queries
- modeling data
- mult-index
- ACID transactions: Atomic, Consistent, Isolated, Durable

don't use for:
- large data
- storing different formats
- high throughput
- flexible schema
- high availability
- horizontal scalability


### PostgreSQL & `psycopg2`

- if running postgres in docker need to install `psycopg2-binary` because postgres is not installed on the machine

this is how queries are parameterized using `psycopg2`
```python
cur.execute("%s, %s", (object1, object2))
```

primary key is the same as unique and not null

create a reference in a fact table using `REFERENCE table(foreign_key_column)`

insert statements `ON CONFLICT DO ____`

### NoSQL
examples:
- apache cassandra (partition row store)
- mongodb (document store)
- dynamodb (key-value store)
- apache hbase (wide column store)
- Neo4j (graph db)

cassandra:
- keyspace - collection of tables
- tables
- rows
- partition - unit of access
- primary key
- columns
    - clustering and data

use me when:
- large amounts of data
- scalability
- throughput
- flexible schema
- availability

dont use me when:
- need ACID
- need to joins
- aggregations
- not easy to change
- small data

data modeling
-------------

OLAP vs OLTP
- online analytical processing
    - analytics and ad hoc queries
- online transaction processing
    - less complex queries in large volume

normalization 
- reduce data redundancy & integrity
- reduce refactoring

normal forms
1NF 
- atomic values
- add data without altering tables
- separate relations into tables
- keep a foreign key
2NF
- 1NF
- all columns rely on primary key
3NF
- 2NF 
- no duplicate data

denormalization - for read heavy workloads

fact and dimension tables
star schema - simplest data schema
snowflake schema - not simplest data schema

not null -> col cant be null
unique -> col has unique values
primary key -> this column is not null and unique

can have a composite key `PRIMARY KEY (col1, col2)`

on conflict do nothing
on conflict do update

nosql db design
---------------

need copies of data

CAP
- consistency
    - database will get the latest piece of data requested
- availability
    - every reequest is recieved 
- partition tolerance
    - network connectivity doesn't affect the system

### cql: no joins, no groupby, no subqueries

queries first -> no join capability

need denormalization

1 table per query

if primary key isn't unique, queries will fail

the sequence of the columns should reflect how the data is partitioned
- the primary key, especially when compisite should have those columns first in the CREATE sequence

clustering columns determine sort order within partition

the partitioning key must be included in query

clustering columns can be used in order of appearance

query without where clause will error

