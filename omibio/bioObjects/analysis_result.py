from omibio.bioObjects.seq_interval import SeqInterval
from dataclasses import dataclass
from typing import Callable


@dataclass
class AnalysisResult:
    intervals: list[SeqInterval] = None
    meta: dict = None
    _plot_func: Callable | None = None

    def plot(self, **kwargs):
        if self._plot_func is None:
            raise NotImplementedError(
                "Plotting is not supported for this analysis."
            )
        return self._plot_func(self, **kwargs)
