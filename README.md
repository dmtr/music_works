# Works Single View

## Instructions 

Build service:

`docker-compose build`

Start service:

`docker-compose up -d`

Load and reconsile data:

`docker-compose run --rm app python manage.py load_works ./data/works_metadata.csv`

## Q&A

> Describe briefly the matching and reconciling method chosen.

1. Try to find work by iswc in database
1. If found update contributors
1. If not found try to find work by title and contributors
1. If found update contributors

> We constantly receive metadata from our providers, how would you automatize the process?

It depends on how metadata is provided. In simple case when metadata is provided in files
periodic task can check new files in particular folder and process this files. Processing can be done in parallel.

> Imagine that the Single View has 20 million musical works, do you think your solution would have a similar response time?

Obviously response time will increase and it is difficult to say how without testing.
I believe that well configured PostgreSQL running on appropriate hardware can handle such workload.

> If not, what would you do to improve it?

First I will analyze SQL query execution. Maybe it is necessary to add (or remove) index (indexes).
Second I will think about using another type of database (maybe Elasticsearch).

## Future improvements
1. Dockerfile is not production ready
1. Add py.test
1. Add OpenAPI documentation
