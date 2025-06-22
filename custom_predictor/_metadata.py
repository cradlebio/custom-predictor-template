import dataclasses


@dataclasses.dataclass(frozen=True)
class CustomPredictorInput:
    """Specifies an input parameter for a custom predictor.

    Input paramaters are passed as command-line arguments to the predictor.

    Args:
        name: The name of the input parameter.
        type: The data type of the parameter. Must be one of `bool`, `int`, `float` or `str`.
        default: The default value of the parameter, or `None` to make it a required parameter.
    """

    name: str
    type: type[bool | int | float | str]
    default: None | bool | int | float | str = None


@dataclasses.dataclass(frozen=True)
class CustomPredictorMetadata:
    """Metadata for the custom predictor, used for importing into Cradle

    Args:
        name: Name of the custom predictor with which it will be registered in Cradle.
              Must only consist of lowercase letters, numbers and the '-' character.
        display_name: Human-readable name of the predictor.
        description: Description of what the predictor does
        author: Author of the custom predictor (in the format `First Last <email@domain.tld>`)
        url: Optional field to set a URL where to find more information about the predictor
        inputs: A tuple of inputs that must be provided to the custom predictor when starting
                a task that uses it.
        outputs: Outputs of the custom predictor. The length of this tuple specifies the number
                 of outputs that the predictor generates for each sequence. The type of each
                 output is always of type `float`.
        batch_size: Maximum number of sequences that the custom predictor is invoked with at a time
        cpu_mcores: CPU usage to allocate when running the custom predictor, in millicores
        main_memory_mib: Main memory, in MiB, to make available to the custom predictor at runtime
        gpu_memory_mib: GPU memory, in MiB, to make available to the custom predictor at runtime
    """

    name: str
    display_name: str
    description: str
    author: str
    url: str | None
    inputs: tuple[CustomPredictorInput, ...]
    outputs: tuple[str, ...]
    batch_size: int
    cpu_mcores: int
    main_memory_mib: int
    gpu_memory_mib: int
