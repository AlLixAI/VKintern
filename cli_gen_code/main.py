import sys

import click
from pydantic import ValidationError

from controller_generator import generate_controllers
from pydantic_generator import generate_models
from json_schema_validator import validate_json_schema, validate_document

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

@click.group()
def cli():
    pass

@click.command()
@click.option('-json-schema-dir', required=True, type=click.Path(exists=True), help='Path to the JSON schema file.')
@click.option('-out-dir', required=True, type=click.Path(), help='Output directory for the generated models.')
def gen_models(json_schema_dir, out_dir):
    try:
        validate_json_schema(json_schema_dir)
        validate_document(json_schema_dir)
        try:
            generate_models(json_schema_dir, out_dir)
            click.echo(f"Модель pydantic успешно сгенерирована и сохранена в {out_dir}")
        except Exception as e:
            click.echo(f"Ошибка генерации {e}")
    except ValidationError as e:
        click.echo(f"Проблема с типом Document: {e}")
    except ValueError as e:
        click.echo(f"Проблема с JSON: {e}")
    except Exception as e:
        click.echo(f"Какая-то ошибка: {e}")

@click.command()
@click.option('-models', required=True, help='Directory containing the generated models.')
@click.option('-rest-routes', required=True, help='Output directory for the generated routes.')
def gen_rest(models, rest_routes):
    try:
        generate_controllers(models, rest_routes)
        click.echo(f"Контроллеры успешно сгенерированы в {rest_routes}")
    except Exception as e:
        click.echo(f"Произошла ошибка {e}")

cli.add_command(gen_models)
cli.add_command(gen_rest)

if __name__ == '__main__':
    cli()