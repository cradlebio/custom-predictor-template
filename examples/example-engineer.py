"""A snippet using the Cradle SDK for creating an engineer task with custom predictor filterers.

Custom predictors are only available via the SDK. This code snippet demonstrates how to create
a task that optimizes a template sequence based on a single property with a previously-trained model.
It then configures a filterer such that only sequences that pass a threshold on the custom predictor
result are generated.

Once the task has been created, you can see it in the Cradle platform (web interface)
under the specified project and round.

Look for the places highlighted with `!!!` where a change/review to adapt for specific
circumstances is necessary.
"""

from cradle.sdk.client import Client
from cradle.sdk.types.common import ContextRound
from cradle.sdk.types.task import TaskCreate
from cradle.sdk.types.tasks.common import TaskState
from cradle.sdk.types.tasks.v2 import (
    Constraint,
    CustomPredictorParam,
    EngineerParameters,
    ScoreBasedRanker,
    Measure,
    ModelBasedGenerator,
    MonomerAssembly,
    MonomerScorerConfig,
    MonomerSamplingTemplate,
    MonomerScorerRef,
    OptimizationDirection,
    PrimaryObjective,
    RelativeTo,
    ScoreBasedFilterer,
    TrainResult,
)

workspace_name = "<Workspace name>"  # !!! Insert your workspace name
project_name = "<Project Name>"  # !!! Insert project name
round_name = "<Round Name>"  # !!! Insert round name

# Sets up client for the workspace.
client = Client(base_url="https://api.cradle.bio", workspace=workspace_name)

# Retrieves the project and round. Both are assumed to exist already.
project = next((p for p in client.project.list() if p.name == project_name), None)
assert project is not None
project_round = next(
    (r for r in client.round.list(project_id=project.id) if r.name == round_name),
    None,
)
assert project_round is not None

# Use the first custom predictor from the list
cp = next(client.custom_predictor.list(), None)  # !!! Pick the right one if you have multiple
assert cp is not None

# Grab and print relevant info.
cp_version = cp.root.version_id
cp_outputs = cp.root.outputs
print(cp_outputs)
cp_output = cp.root.outputs[0]
cp_inputs = cp.root.inputs
print(cp_inputs)
cp_name = cp.root.name
print(cp_name)
print(cp.root.description)

# Specify the template to engineer (optimize).
template_sequence = "..."  # !!! Pass the template you wish to optimize here.

# We assume the sequence is a monomer here (e.g., scfv, vhh). If you are working
# with vh-vls, make sure to replace everything that is prefixed with
# `Monomer` below to the corresponding `VhVl` version.
template_monomer = MonomerAssembly(monomer=template_sequence)

train_task = next(
    (t for t in client.task.list(round_id=project_round.id) if t.type == "train/v2" and t.state == TaskState.COMPLETED),
    None,
)  # !!! Make sure to pick the correct training task if there are multiple
assert train_task is not None

train_result = train_task.result
assert isinstance(train_result, TrainResult)
assert train_result.models.scorer is not None

# Define the generator in the engineer algorithm.
engineer_generator = ModelBasedGenerator(
    template=MonomerSamplingTemplate(
        assembly=template_monomer,
        sampler=train_result.models.sampler,
    ),
    requirements=[],
    discourage_mutations=None,
    min_mutations=1,
    max_mutations=8,
)

# Define the ranker in the engineer algorithm.
primary_assay_id = "..."  # !!! Pass the assay ID you want to optimize, must be one of the assays from the training task
direction = OptimizationDirection.MAXIMIZE  # !!! Change if you want to minimize instad.
engineer_ranker = ScoreBasedRanker(
    primary_objective=PrimaryObjective(
        measure=Measure(assay_id=primary_assay_id, direction=direction),
        reference=RelativeTo(reference=template_monomer),
    ),
    constraints=[],  # !!! No constraints in this minimal example. Add them here for your own run.
    scorer_config=MonomerScorerConfig(
        scorer=train_result.models.scorer,
        controls=None,
    ),
)

# Define the filterers in the engineer algorithm. Below we set a single
# constraint on the custom predictor output (keep below template).
engineer_filterers = [
    ScoreBasedFilterer(
        scorer=MonomerScorerRef(
            scorer=CustomPredictorParam(
                name=cp_name,
                version_id=cp_version,
            )
        ),
        constraints=[
            Constraint(
                measure=Measure(
                    assay_id=cp_output.assay_id,
                    direction=OptimizationDirection.MINIMIZE,
                ),
                threshold=RelativeTo(
                    reference=template_monomer,
                    margin=1.0,
                ),
            ),
        ],
    )
]

# Create engineer task, or return task if it exists already
engineer_response = client.task.create_or_get(
    TaskCreate(
        context=ContextRound(round_id=project_round.id),
        parameters=EngineerParameters(
            generator=engineer_generator,
            ranker=engineer_ranker,
            filterers=engineer_filterers,
            num_assemblies=5,  # !!! Increase this for a real run.
        ),
        display_name="Engineer with custom predictor smoke test",
        # !!! Add an idempotency key here to uniquely identify your run: No two
        # tasks can exist with the same `idempotency_key`.
        idempotency_key="engineer_cp_smoke_test",
    ),
)
print(engineer_response.id)
