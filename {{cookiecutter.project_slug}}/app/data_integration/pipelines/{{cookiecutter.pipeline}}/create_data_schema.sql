DROP SCHEMA IF EXISTS {{cookiecutter.pipeline_slug}}_data CASCADE;

CREATE SCHEMA {{cookiecutter.pipeline_slug}}_data;

SELECT util.create_chunking_functions('{{cookiecutter.pipeline_slug}}_data');
