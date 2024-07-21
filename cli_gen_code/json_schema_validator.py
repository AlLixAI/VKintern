import json
import jsonschema

from pydantic import ValidationError

from models.schemas_default import Document


def validate_document(json_schema_dir):
    with open(json_schema_dir, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    try:
        doc = Document(**schema)
        print("Документ необходимого формата валиден по спецификации.")
    except ValidationError as e:
        raise ValidationError(f"Ошибка валидации: {e}")


def validate_json_schema(json_schema_dir):
    with open(json_schema_dir, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    validator = jsonschema.Draft7Validator(schema)

    errors = list(validator.iter_errors(schema))
    if errors:
        for error in errors:
            print(f"Validation error: {error.message}")
        raise ValueError(f"Документ не валиден по JSON Schema Draft 7.")
    else:
        print(f"Документ валиден по базовой валидности.")