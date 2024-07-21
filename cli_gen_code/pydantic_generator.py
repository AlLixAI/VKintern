import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

def generate_models(json_schema_file, out_dir):
    with open(json_schema_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(['py'])
    )

    classes = defaultdict(dict)
    class_structure(json_data['configuration']['specification'], classes, f"{json_data['kind']}Specification")
    class_structure(json_data['configuration']['settings'], classes, f"{json_data['kind']}Settings")


    template = env.get_template('model_gen.j2')
    rendered_code = template.render(
        model_name=json_data['kind'],
        classes=classes
    )

    model_name = json_data['kind'].replace(':', '_')
    model_file_path = os.path.join(out_dir, f"{model_name}_model.py")
    os.makedirs(os.path.dirname(model_file_path), exist_ok=True)

    with open(model_file_path, 'w', encoding='utf-8') as model_file:
        model_file.write(rendered_code)

def type_check(field_value):
    if isinstance(field_value, str):
        return "str"
    elif isinstance(field_value, int):
        return "int"
    elif isinstance(field_value, bool):
        return "bool"
    elif isinstance(field_value, list):
        inner_type = type_check(field_value[0]) if field_value else "Any"
        return f"List[{inner_type}]"
    elif isinstance(field_value, dict):
        return "Dict[Any, Any]"
    else:
        return "Any"

def class_structure(fields, classes, class_name):
    for field_name, field_value in fields.items():
        if isinstance(field_value, dict) and field_value:
            sub_class_name = f"{class_name}_{field_name.capitalize()}"
            classes[class_name][field_name] = sub_class_name
            class_structure(field_value, classes, sub_class_name)
        else:
            classes[class_name][field_name] = type_check(field_value)