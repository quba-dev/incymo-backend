from planout.experiment import SimpleExperiment
from planout.ops.random import UniformChoice

from incymo_backend.enums import ItemsEnum


class TestExperiment(SimpleExperiment):
    """The test experiment class."""

    def assign(self, params, userid):
        """Assigning a new experiment."""
        params.items = UniformChoice(
            choices=list(map(lambda x: x.name, ItemsEnum)),
            unit=userid
        )
