import datetime

import data_integration.config
import mara_db.config
import mara_db.dbs
from mara_app.monkey_patch import patch

import app.config


@patch(mara_db.config.databases)
def databases():
    return {
        # the project requires two databases: 'mara' for the app itself, and 'dwh' for the etl
        '{{cookiecutter.default_db_alias}}': mara_db.dbs.PostgreSQLDB(user='stade', host='localhost',
                                                                      database='{{cookiecutter.project_slug.replace("-", "_")}}_{{cookiecutter.default_db_alias}}'),
        'mara': mara_db.dbs.PostgreSQLDB(user='stade', host='localhost',
                                         database='{{cookiecutter.project_slug.replace("-", "_")}}_mara')
    }


# How many cores to use for running the ETL, defaults to the number of CPUs of the machine
# On production, make sure the ETL does not slow down other services too much
patch(data_integration.config.max_number_of_parallel_tasks)(lambda: 4)

patch(app.config.first_date)(lambda: datetime.date.today() - datetime.timedelta(days=5))

# Whether it is possible to run the ETL from the web UI
# Disable on production
patch(data_integration.config.allow_run_from_web_ui)(lambda: True)
