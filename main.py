import yaml
import pdb


def load_yaml(path: str) -> dict:
    """Read a YAML schema into a Python dictionary."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def find_quantity_classes(schema: dict) -> dict:
    """
    Identify classes representing quantities — i.e. having exactly
    'value', 'unit', and 'multiplier' attributes.
    """
    quantity_classes = {}
    for cls_name, cls_data in schema.get("classes", {}).items():
        attrs = cls_data.get("attributes", {})
        if set(attrs.keys()) == {"value", "unit", "multiplier"}:
            quantity_classes[cls_name] = cls_data
    return quantity_classes


def replace_quantity_classes(
    schema: dict, ucum_map: dict, quantity_classes: dict
) -> dict:
    """Replace quantity class references with decimal + UCUM unit."""
    for _, cls_data in schema.get("classes", {}).items():
        attrs = cls_data.get("attributes", {})
        for _, attr_data in attrs.items():
            rng = attr_data.get("range")
            if rng in quantity_classes:
                unit_code = ucum_map.get(rng, "1")
                attr_data["range"] = "decimal"
                attr_data["unit"] = {"ucum_code": unit_code}
    return schema


def delete_classes(schema: dict, classes_to_delete: dict) -> None:
    """Delete all classes_to_delete from the schema - inplace."""
    for qclass in classes_to_delete.keys():
        schema.get("classes", {}).pop(qclass, None)


if __name__ == "__main__":
    schema = load_yaml("schema/im_tc57cim.yml")
    quantities = find_quantity_classes(schema)
    ucum_map = load_yaml("mapping-quantities-to-ucum.yml")
    updated = replace_quantity_classes(schema, ucum_map, quantities)
    delete_classes(updated, quantities)
    yaml.safe_dump(updated, open("cim-with-ucum.yml", "w"))
