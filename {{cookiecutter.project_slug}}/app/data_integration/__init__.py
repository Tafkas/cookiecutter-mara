"""Configures the data integration pipelines of the project"""

import datetime
import functools

import data_integration.config
import etl_tools.config
from data_integration.pipelines import Pipeline
from mara_app.monkey_patch import patch

import app.config

patch(data_integration.config.data_dir)(lambda: app.config.data_dir())
patch(data_integration.config.first_date)(lambda: app.config.first_date())
patch(data_integration.config.default_db_alias)(lambda: '{{cookiecutter.default_db_alias}}')


@patch(data_integration.config.root_pipeline)
@functools.lru_cache(maxsize=None)
def root_pipeline():
    import app.data_integration.pipelines.utils
    import app.data_integration.pipelines.{{cookiecutter.pipeline}}

    pipeline = Pipeline(
        id='{{cookiecutter.project_slug.replace("-", "_")}}',
        description='{{cookiecutter.project_name}} Data Pipeline')

    pipeline.add(app.data_integration.pipelines.utils.pipeline)
    pipeline.add(app.data_integration.pipelines.{{cookiecutter.pipeline}}.pipeline, upstreams=['utils'])
    return pipeline


patch(etl_tools.config.number_of_chunks)(lambda: 11)
patch(etl_tools.config.first_date_in_time_dimensions)(lambda: app.config.first_date())
patch(etl_tools.config.last_date_in_time_dimensions)(
    lambda: datetime.datetime.utcnow().date() - datetime.timedelta(days=1))
