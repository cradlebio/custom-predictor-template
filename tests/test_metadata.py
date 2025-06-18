import re

from predictor import CustomPredictorMetadata

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
DNS1123_PATTERN = re.compile("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
MAX_INPUTS = 64
MAX_OUTPUTS = 64
MAX_CPU_MCORES = 8000
MAX_MAIN_MEMORY_MIB = 64 * 1024 * 1024 * 1024
MAX_GPU_MEMORY_MIB = 16 * 1024 * 1024 * 1024


def test_metadata():
    metadata = CustomPredictorMetadata()
    assert len(metadata.name) <= MAX_NAME_LENGTH
    assert len(metadata.name) > 0
    assert DNS1123_PATTERN.match(metadata.name), (
        "Predictor name must consist only of small letters, numbers and the '-' character"
    )
    assert len(metadata.display_name) > 0
    assert len(metadata.description) <= MAX_DESCRIPTION_LENGTH
    assert len(metadata.inputs) <= MAX_INPUTS
    assert len(metadata.outputs) > 0
    assert len(metadata.outputs) <= MAX_OUTPUTS

    assert all(x.type in (bool, int, float, str) for x in metadata.inputs)

    assert metadata.cpu_mcores > 0
    assert metadata.cpu_mcores <= MAX_CPU_MCORES
    assert metadata.main_memory_mib > 0
    assert metadata.main_memory_mib <= MAX_MAIN_MEMORY_MIB
    assert metadata.gpu_memory_mib >= 0
    assert metadata.gpu_memory_mib <= MAX_GPU_MEMORY_MIB
