

## GCE (Google Cloud Engine)
* [Create Instance](https://cloud.google.com/compute/docs/quickstart-linux)
* [Create app & deploy on GCA](https://cloud.google.com/appengine/docs/standard/python3/quickstart)
* [Main config file app.yaml](https://cloud.google.com/appengine/docs/standard/python3/config/appref#directory_structure)
* [Cloud SQL quickstart](https://cloud.google.com/sql/docs/mysql/quickstart)

## CGE common used commands
* `gcloud sql instances list`		(instance list)
* `gcloud app logs tail`		    (google app engine logs)
* `gcloud app deploy`               (deploy app on GAE)

___

## Project structure
```
├── app.yaml                        (CGE main configuration file note: service: mb-app(name which is deployed on the GAE))
├── config
│   └── constants.py                (csv, sql, db constants)
├── docker 
│   ├── docker-compose.yml          (mysql database installed from docker)
│   └── sql
│       ├── cv_log.csv
│       ├── ddl.sql
│       └── purchase_log.csv
├── libs
│   ├── controller.py
│   └── mysqldb.py                  (sqlalchemy)
├── main.py
├── pages
│   ├── index.py                    (api, report)
│   └── other.py                    (execute ddl, import csv)
├── readme.md
├── requirements.txt                
└── templates
    └── index.html                  (template page)
```

## How to execute

### Docker
```
docker-compose up -d
```

### Database script execute
```
localhost:8080/createsql
localhost:8080/importcsv
```
* execute ddl & import csv file data

### Execute python program
```
python3 main.py
```