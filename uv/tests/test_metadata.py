import re

from custom_predictor._processor import METADATA

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
DNS1123_PATTERN = re.compile("^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")
MAX_INPUTS = 64
MAX_OUTPUTS = 64
MAX_CPU_MCORES = 8000
MAX_MAIN_MEMORY_MIB = 64 * 1024 * 1024 * 1024
MAX_GPU_MEMORY_MIB = 16 * 1024 * 1024 * 1024


def test_metadata():
    assert len(METADATA.name) <= MAX_NAME_LENGTH
    assert len(METADATA.name) > 0
    assert DNS1123_PATTERN.match(METADATA.name), (
        "Predictor name must consist only of small letters, numbers and the '-' character"
    )
    assert len(METADATA.display_name) > 0
    assert len(METADATA.description) <= MAX_DESCRIPTION_LENGTH
    assert len(METADATA.inputs) <= MAX_INPUTS
    assert len(METADATA.outputs) > 0
    assert len(METADATA.outputs) <= MAX_OUTPUTS

    assert all(x.type in (bool, int, float, str) for x in METADATA.inputs)

    assert METADATA.cpu_mcores > 0
    assert METADATA.cpu_mcores <= MAX_CPU_MCORES
    assert METADATA.main_memory_mib > 0
    assert METADATA.main_memory_mib <= MAX_MAIN_MEMORY_MIB
    assert METADATA.gpu_memory_mib >= 0
    assert METADATA.gpu_memory_mib <= MAX_GPU_MEMORY_MIB
