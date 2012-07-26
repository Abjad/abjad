from abjad.tools import abctools
from experimental.quantizationtools.MeasurewiseQSchema import MeasurewiseQSchema
from experimental.quantizationtools.QEventSequence import QEventSequence
from experimental.quantizationtools.QSchema import QSchema


class Quantizer(abctools.AbjadObject):

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, q_schema=None, grace_handler=None):

        q_event_sequence = QEventSequence(q_event_sequence)

        if q_schema is None:
            q_schema = MeasurewiseQSchema()
        assert isinstance(q_schema, QSchema)

        if grace_handler is None:
            grace_handler = GraceHandler()
        assert isinstance(grace_handler, GraceHandler)

        q_target = q_schema(q_event_sequence.duration_in_ms)
        q_result = q_target(q_event_sequence, grace_handler)
