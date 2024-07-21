import os
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape


def generate_controllers(models_dir, routes_dir):

    file_loader = FileSystemLoader('templates')
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(['py'])
    )

    generated_files = os.listdir(models_dir)

    for model_file in generated_files:
        if model_file.endswith('.py'):
            model_name = model_file[:-9]
            prefix = model_name.lower()
            tag = model_name.capitalize()

            output_file = os.path.join(routes_dir, f'{prefix}_controllers.py')

            topic = 'quickstrt-event' # Это небольшой костыль.

            context = {
                'prefix': prefix,
                'tag': tag,
                'topic': topic
            }

            template = env.get_template('controller_gen.j2')

            generated_code = template.render(context)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, 'w') as f:
                f.write(generated_code)

