import dataclasses

from predictor.metadata import CustomPredictorMetadata


def dump_metadata():
    metadata = CustomPredictorMetadata()
    for field in dataclasses.fields(metadata):
        if isinstance(field.default, (list, tuple)):
            print(f"{field.name}:")
            for elem in field.default:
                print(f"  {elem}")
        else:
            print(f"{field.name}: {field.default}")


if __name__ == "__main__":
    dump_metadata()
