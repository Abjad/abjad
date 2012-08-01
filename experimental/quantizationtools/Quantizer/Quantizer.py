from abjad.tools import abctools
from experimental.quantizationtools.MeasurewiseQSchema import MeasurewiseQSchema
from experimental.quantizationtools.QEventSequence import QEventSequence
from experimental.quantizationtools.QSchema import QSchema


class Quantizer(abctools.AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        pass    

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, q_schema=None, grace_handler=None,
        heuristic=None, job_handler=None):

        q_event_sequence = QEventSequence(q_event_sequence)

        if q_schema is None:
            q_schema = MeasurewiseQSchema()
        assert isinstance(q_schema, QSchema)

        q_target = q_schema(q_event_sequence.duration_in_ms)

        notation = q_target(q_event_sequence,
            grace_handler=grace_handler,
            heuristic=heuristic,
            job_handler=job_handler)

        return notation
