from ._metadata import CustomPredictorMetadata, CustomPredictorInput

NAME = "custom-predictor-template"

METADATA = CustomPredictorMetadata(
    name=NAME,
    display_name=NAME.replace("-", " ").title(),
    description="This predictor counts the occurence of A and other amino acid subsequences in a sequence",
    author="Cradle <partnerships@cradle.bio>",
    url=None,
    inputs=(
        CustomPredictorInput(name="factor", type=float, default=1.0),
        CustomPredictorInput(name="subseq", type=str),
    ),
    outputs=("As", "Subseqs"),
    batch_size=1024,
    cpu_mcores=100,
    main_memory_mib=128,
    gpu_memory_mib=0,
)


class Processor:
    def __init__(self, params: dict[str, bool | int | float | str]):
        """Called at startup time with the parameter values for the parameters specified in metadata"""
        self._factor = float(params["factor"])
        self._subseq = str(params["subseq"])

    def __call__(self, sequences: list[str], random_seed: int) -> list[list[float]]:
        """Called for every batch of sequences.

        This example predictor has two outputs. The first output is the number of A
        amino acids in the sequence and the second output is the number of E amino
        acids in the sequence.
        """
        del random_seed
        return [
            [self._factor * float(sequence.count("A")), self._factor * float(sequence.count(self._subseq))]
            for sequence in sequences
        ]
