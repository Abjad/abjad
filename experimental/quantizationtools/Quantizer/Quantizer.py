from abjad.tools.abctools import AbjadObject


class Quantizer(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        pass    

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, q_schema=None, grace_handler=None,
        heuristic=None, job_handler=None, attack_point_optimizer=None,
        attach_tempo_marks=True):
        from experimental import quantizationtools

        q_event_sequence = quantizationtools.QEventSequence(q_event_sequence)

        if q_schema is None:
            q_schema = quantizationtools.MeasurewiseQSchema()
        assert isinstance(q_schema, quantizationtools.QSchema)

        q_target = q_schema(q_event_sequence.duration_in_ms)

        notation = q_target(q_event_sequence,
            grace_handler=grace_handler,
            heuristic=heuristic,
            job_handler=job_handler,
            attack_point_optimizer=attack_point_optimizer,
            attach_tempo_marks=attach_tempo_marks,
            )

        #return notation, q_target
        return notation
