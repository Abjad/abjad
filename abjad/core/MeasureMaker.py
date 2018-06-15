from abjad.system.AbjadValueObject import AbjadValueObject


class MeasureMaker(AbjadValueObject):
    r"""
    Measure-maker.

    ..  container:: example

        >>> maker = abjad.MeasureMaker()
        >>> measures = maker([(1, 8), (5, 16), (5, 16)])
        >>> staff = abjad.Staff(measures)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                {   % measure
                    \time 1/8
                    s1 * 1/8
                }   % measure
                {   % measure
                    \time 5/16
                    s1 * 5/16
                }   % measure
                {   % measure
                    s1 * 5/16
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Makers'

    __slots__ = (
        '_implicit_scaling',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, implicit_scaling=False):
        self._implicit_scaling = implicit_scaling

    ### SPECIAL METHODS ###

    def __call__(self, time_signatures):
        """
        Calls measure-maker on ``time_signatures``.

        Returns measures.
        """
        import abjad
        measures = []
        for time_signature in time_signatures:
            time_signature = abjad.TimeSignature(time_signature)
            measure = abjad.Measure(
                time_signature,
                implicit_scaling=self.implicit_scaling,
                )
            measures.append(measure)
        for i, measure in enumerate(measures):
            skip = abjad.Skip(1)
            # allow zero-update iteration
            time_signature = measure.time_signature
            duration = time_signature.duration
            if measure.implicit_scaling:
                implied_prolation = time_signature.implied_prolation
                multiplier = duration.__div__(implied_prolation)
            else:
                multiplier = abjad.Multiplier(duration)
            abjad.attach(multiplier, skip)
            measure[:] = [skip]
            # REMOVE: spanners attach only to leaves:
            #for spanner in measure._get_spanners():
            #    spanner._remove(measure)
        return abjad.select(measures)

    ### PUBLIC PROPERTIES ###

    @property
    def implicit_scaling(self):
        """
        Is true when measure scale implicitly without top-level tuplet.

        Returns true, false or none.
        """
        return self._implicit_scaling
