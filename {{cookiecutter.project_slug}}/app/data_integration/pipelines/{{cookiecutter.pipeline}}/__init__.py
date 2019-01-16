import pathlib

import etl_tools.utils
from data_integration.commands.bash import RunBash
from data_integration.commands.sql import ExecuteSQL
from data_integration.pipelines import Pipeline, Task


pipeline = Pipeline(
    id="{{cookiecutter.pipeline}}",
    description="My first data pipeline",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "{{cookiecutter.pipeline_slug}}"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates the schemas of the pipeline",
         commands=[
             ExecuteSQL(sql_file_name='recreate_schemas.sql'),
             ExecuteSQL(sql_file_name="create_data_schema.sql",
                        file_dependencies=["create_data_schema.sql"])
         ]))

pipeline.add(Task(id='ping_localhost', description='Pings localhost',
                  commands=[RunBash('ping -c 3 localhost')]),
             upstreams=['initialize_schemas'])

pipeline.add_final(
    Task(id="replace_schema",
         description="Replaces the current {{cookiecutter.pipeline_slug}}_dim schema with the contents of {{cookiecutter.pipeline_slug}}_dim_next",
         commands=[
             ExecuteSQL(sql_statement="SELECT util.replace_schema('{{cookiecutter.pipeline_slug}}_dim', '{{cookiecutter.pipeline_slug}}_dim_next');")
         ]))
