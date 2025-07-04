import dataclasses
from typing import Any

from custom_predictor import METADATA


def render(obj: Any) -> str:
    if isinstance(obj, type):
        return obj.__name__
    return "{}".format(obj)


def dump_object(obj: Any, indent: str = ""):
    if dataclasses.is_dataclass(obj):
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            field_display_name = field.name.replace("_", " ").title()

            if isinstance(value, (tuple, list)):
                print("{}{}:".format(indent, field_display_name))
                for i, elem in enumerate(value):
                    if i > 0 and dataclasses.is_dataclass(elem):
                        print("{}---".format(indent + "  "))
                    dump_object(elem, indent=indent + "  ")
            else:
                print("{}{}: {}".format(indent, field_display_name, render(value)))
    else:
        print("{}{}".format(indent, render(obj)))


def dump_metadata():
    dump_object(METADATA)


if __name__ == "__main__":
    dump_metadata()
