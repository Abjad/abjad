from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QSchemaItem import QSchemaItem
from experimental.quantizationtools.SearchTree import SearchTree


class MeasurewiseQSchemaItem(QSchemaItem):
    '''`MeasurewiseQSchemaItem` represents a change of state in the timeline of a metered
    quantization process.

    ::

        >>> from experimental import quantizationtools
        >>> quantizationtools.MeasurewiseQSchemaItem()
        MeasurewiseQSchemaItem()

    Define a change in tempo:

    ::

        >>> quantizationtools.MeasurewiseQSchemaItem(tempo=((1, 4), 60))
        MeasurewiseQSchemaItem(
            tempo=contexttools.TempoMark(
                durationtools.Duration(1, 4),
                60
                ),
            )

    Define a change in time signature:

    ::

        >>> quantizationtools.MeasurewiseQSchemaItem(tempo=((6, 8))
        MeasurewiseQSchemaItem(
            time_signature=contexttools.TimeSignatureMark(
                (6, 8)
                ),
            )

    Test for beatspan, given a defined time signature:

    ::

        >>> _.beatspan
        Duration(1, 8)

    `MeasurewiseQSchemaItem` is immutable.

    Return `MeasurewiseQSchemaItem` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()
    _fields = ('search_tree', 'tempo', 'time_signature', 'use_full_measure')

    ### INITIALIZER ###

    def __new__(klass, search_tree=None, tempo=None, time_signature=None, use_full_measure=None):
        
        if search_tree is not None:
            search_tree = SearchTree(search_tree)

        if tempo is not None:
            tempo = contexttools.TempoMark(tempo)
            assert not tempo.is_imprecise

        if time_signature is not None:
            time_signature = contexttools.TimeSignatureMark(time_signature)

        if use_full_measure is not None:
            use_full_measure = bool(use_full_measure)

        return tuple.__new__(klass, (search_tree, tempo, time_signature, use_full_measure))

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def beatspan(self):
        '''The beatspan duration, if a time signature was defined.

        Return `Duration` or `None`.
        '''
        if self.time_signature is not None:
            if self.use_full_measure:
                return self.time_signature.duration
            else:
                return durationtools.Duration(1, self.time_signature.denominator)
        return None

    @property
    def search_tree(self):
        '''The optionally defined search tree.

        Return `SearchTree` or `None`.
        '''
        return self[0]

    @property
    def tempo(self):
        '''The optionally defined `TempoMark`.

        Return `TempoMark` or `None`.
        '''
        return self[1]

    @property
    def time_signature(self):
        '''The optionally defined TimeSignatureMark.

        Return `TimeSignatureMark` or None.
        '''
        return self[2]

    @property
    def use_full_measure(self):
        '''If True, use the full measure as the beatspan.

        Return bool or None.
        '''
        return self[3]
