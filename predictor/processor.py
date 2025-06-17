class Processor:
    def __init__(self, params: dict[str, bool | int | float | str]):
        """Called at startup time with the parameter values for the parameters specified in metadata"""
        del params

    def __call__(self, sequences: list[str], random_seed: int) -> list[tuple[float, ...]]:
        """Called for every batch of sequences.

        This example predictor has two outputs. The first output is the number of A
        amino acids in the sequence and the second output is the number of E amino
        acids in the sequence.
        """
        del random_seed
        return [(float(sequence.count("A")), float(sequence.count("E"))) for sequence in sequences]
