# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools
from abjad.tools.quantizationtools.QSchemaItem import QSchemaItem


class MeasurewiseQSchemaItem(QSchemaItem):
    '''`MeasurewiseQSchemaItem` represents a change of state in the
    timeline of a metered quantization process.

    ::

        >>> q_schema_item = quantizationtools.MeasurewiseQSchemaItem()
        >>> print(format(q_schema_item))
        quantizationtools.MeasurewiseQSchemaItem()

    Define a change in tempo:

    ::

        >>> q_schema_item = quantizationtools.MeasurewiseQSchemaItem(
        ...     tempo=((1, 4), 60),
        ...     )
        >>> print(format(q_schema_item))
        quantizationtools.MeasurewiseQSchemaItem(
            tempo=indicatortools.Tempo(
                reference_duration=durationtools.Duration(1, 4), 
                units_per_minute=60,
                ),
            )

    Define a change in time signature:

    ::

        >>> q_schema_item = quantizationtools.MeasurewiseQSchemaItem(
        ...     time_signature=(6, 8),
        ...     )
        >>> print(format(q_schema_item))
        quantizationtools.MeasurewiseQSchemaItem(
            time_signature=indicatortools.TimeSignature((6, 8)),
            )

    Test for beatspan, given a defined time signature:

    ::

        >>> q_schema_item.beatspan
        Duration(1, 8)

    `MeasurewiseQSchemaItem` is immutable.

    Return `MeasurewiseQSchemaItem` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_time_signature',
        '_use_full_measure',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        search_tree=None,
        tempo=None,
        time_signature=None,
        use_full_measure=None
        ):
        QSchemaItem.__init__(
            self,
            search_tree=search_tree,
            tempo=tempo,
            )
        if time_signature is not None:
            time_signature = indicatortools.TimeSignature(time_signature)
        self._time_signature = time_signature
        if use_full_measure is not None:
            use_full_measure = bool(use_full_measure)
        self._use_full_measure = use_full_measure

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        r'''The beatspan duration, if a time signature was defined.

        Returns duration or none.
        '''
        if self.time_signature is not None:
            if self.use_full_measure:
                return self.time_signature.duration
            else:
                return durationtools.Duration(
                    1, self.time_signature.denominator)
        return None

    @property
    def time_signature(self):
        r'''The optionally defined TimeSignature.

        Returns time signature or none
        '''
        return self._time_signature

    @property
    def use_full_measure(self):
        r'''If True, use the full measure as the beatspan.

        Returns boolean or none.
        '''
        return self._use_full_measure
