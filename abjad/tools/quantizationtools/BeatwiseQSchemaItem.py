# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.quantizationtools.QSchemaItem import QSchemaItem


class BeatwiseQSchemaItem(QSchemaItem):
    '''Beatwise q-schema item.

    Represents a change of state in the timeline of an unmetered quantization
    process.

    ::

        >>> import abjad
        >>> from abjad.tools import quantizationtools

    ::

        >>> q_schema_item = quantizationtools.BeatwiseQSchemaItem()
        >>> f(q_schema_item)
        quantizationtools.BeatwiseQSchemaItem()

    ..  container:: example

        Defines a change in tempo:

        ::

            >>> q_schema_item = quantizationtools.BeatwiseQSchemaItem(
            ...     tempo=((1, 4), 60),
            ...     )
            >>> f(q_schema_item)
            quantizationtools.BeatwiseQSchemaItem(
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                )

    ..  container:: example

        Defines a change in beatspan:

        ::

            >>> q_schema_item = quantizationtools.BeatwiseQSchemaItem(
            ...     beatspan=(1, 8),
            ...     )
            >>> f(q_schema_item)
            quantizationtools.BeatwiseQSchemaItem(
                beatspan=abjad.Duration(1, 8),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beatspan',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        beatspan=None,
        search_tree=None,
        tempo=None,
        ):
        QSchemaItem.__init__(
            self,
            search_tree=search_tree,
            tempo=tempo,
            )
        if beatspan is not None:
            beatspan = durationtools.Duration(beatspan)
            assert 0 < beatspan
        self._beatspan = beatspan

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        r'''The optionally defined beatspan duration.

        Returns duration or none.
        '''
        return self._beatspan
