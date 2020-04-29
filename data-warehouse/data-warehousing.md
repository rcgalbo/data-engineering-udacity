
warehouses
----------

operational databases
- too slow for analytics
- to difficult to understand

OLAP vs OLTP
- analytics processing vs transaction processing

data warehouse is a system for supporting analytical processes
- a copy of trasaction data structured for query and analysis

data warehouse traits:

- easy to understand
- performs
- qa
- handles new questions
- secure

fact table -> numeric or additive
dimension tables -> attributes


kimbal bus architecture: data is organized by business process, used across departments
- atomic and summary data

independent data marts: everyone has their own process

corporate information factory (CIF)
- normalized backend
- data delivery -> specific datamarts
- data marts are mostly aggregated
- source -> 3nf db -> department data marts

hybrid bus CIF: 
- source -> 3nf -> enterprise dw

olap cubes
- aggregations of fact over multiple dimensions
olap opperations: 
- rollup - summarize over a dimension
- drill-down - increase number of dimensions more descrite
- slice - filter on a specific dimension
- dice - take range of a specific dimension

`group by CUBE(x1,x2)` gives all gropings across all combinations of columns


DWH on AWS

redshift
- postgres on the inside
- col store
- 1 query across many cpus
- nodes have slices - cpus
- n slices can have n partitions

sql to sql etl ~ park csv in s3

transfer from s3 to redshift using COPY

if files are large: break it up, parallel ingest
- use either common prefix or manifest file

can `UNLOAD` data to s3 also

infrastructure as code - devops