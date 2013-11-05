# -*- encoding: utf-8 -*-
import collections
import copy
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools.timeintervaltools.TimeIntervalMixin import TimeIntervalMixin


class TimeInterval(TimeIntervalMixin, collections.MutableMapping):
    r'''A start_offset / stop_offset pair, carrying some metadata.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_data',
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            start_offset, stop_offset, data = args[0].start_offset, args[0].stop_offset, args[0]
        elif len(args) == 2:
            start_offset, stop_offset, data = args[0], args[1], {}
        elif len(args) == 3:
            start_offset, stop_offset, data = args[0], args[1], args[2]

        start_offset, stop_offset = durationtools.Offset(start_offset), durationtools.Offset(stop_offset)
        assert start_offset < stop_offset
        if isinstance(data, type(self)):
            data = data._data
        assert isinstance(data, dict)

        self._start = start_offset
        self._stop = stop_offset
        self._data = copy.copy(data)

    ### SPECIAL METHODS ###

    def __delitem__(self, item):
        self._data.__delitem__(item)

    def __eq__(self, expr):
        if type(expr) == type(self) and \
            expr.start_offset == self.start_offset and \
            expr.stop_offset == self.stop_offset and \
            expr._data == self._data:
                return True
        return False

    def __getitem__(self, item):
        return self._data.__getitem__(item)

    def __hash__(self):
        return id(self)

    def __iter__(self):
        for x in self._data:
            yield x

    def __len__(self):
        return len(self._data)

    def __ne__(self, expr):
        return not self.__eq__(expr)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (
            self._class_name, self.start_offset, self.stop_offset, self._data)

    def __setitem__(self, item, value):
        self._data.__setitem__(item, value)

    ### PUBLIC PROPERTIES ###

    @property
    def center(self):
        r'''Center point of start_offset and stop_offset bounds.
        '''
        return durationtools.Offset(self.stop_offset + self.start_offset) / 2

    @property
    def duration(self):
        r'''stop_offset bound minus start_offset bound.
        '''
        return durationtools.Duration(self.stop_offset - self.start_offset)

    @property
    def signature(self):
        r'''Tuple of start_offset bound and stop_offset bound.
        '''
        return (self.start_offset, self.stop_offset)

    @property
    def start_offset(self):
        r'''start_offset bound.
        '''
        return self._start

    @property
    def stop_offset(self):
        r'''stop_offset bound.
        '''
        return self._stop

    @property
    def storage_format(self):
        r'''Storage format of time interval.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        pieces = []
        pieces.append('{}('.format(self._tools_package_qualified_class_name))
        pieces.append('\t{!r},'.format(self.start_offset))
        pieces.append('\t{!r},'.format(self.stop_offset))

        if len(self):
            pieces.append('\t{')

            for key, value in self.iteritems():
                if isinstance(key, abctools.AbjadObject):
                    key = key._tools_package_qualified_repr
                else:
                    key = repr(key)
                if isinstance(value, abctools.AbjadObject):
                    vpieces = value._get_tools_package_qualified_repr_pieces()
                    if 1 < len(vpieces):
                        pieces.append('\t\t{}: {}'.format(key, vpieces[0]))
                        for piece in vpieces[1:-1]:
                            pieces.append('\t\t{}'.format(piece))
                        pieces.append('\t\t{},'.format(vpieces[-1]))
                    else:
                        pieces.append('\t\t{}: {},'.format(key, vpieces[0]))
                else:
                    pieces.append('\t\t{}: {!r},'.format(key, value))

            pieces.append('\t})')

        else:
            pieces.append('\t)')
        return pieces

    ### PUBLIC METHODS ###

    def quantize_to_rational(self, rational):
        rational = durationtools.Duration(rational)
        assert 0 < rational
        start_offset = durationtools.Offset(
            int(round(interval.start_offset / rational))) * rational
        stop_offset = durationtools.Offset(
            int(round(interval.stop_offset / rational))) * rational
        if start_offset == stop_offset:
            stop_offset = start_offset + rational
        return type(self)(start_offset, stop_offset, self)

    def scale_by_rational(self, rational):
        rational = durationtools.Duration(rational)
        assert 0 < rational
        if rational != 1:
            new_duration = (self.stop_offset - self.start_offset) * rational
            return type(self)(self.start_offset, self.start_offset + new_duration, self)
        else:
            return self

    def scale_to_rational(self, rational):
        rational = durationtools.Duration(rational)
        assert 0 < rational
        if rational != self.duration:
            return type(self)(self.start_offset, self.start_offset + rational, self)
        else:
            return self

    def shift_by_rational(self, rational):
        rational = durationtools.Duration(rational)
        if rational != 0:
            return type(self)(
                self.start_offset + rational, self.stop_offset + rational, self)
        else:
            return self

    def shift_to_rational(self, rational):
        rational = durationtools.Offset(rational)
        if rational != self.start_offset:
            duration = self.stop_offset - self.start_offset
            return type(self)(rational, rational + duration, self)
        else:
            return self

    def split_at_rationals(self, *rationals):
        rationals = [durationtools.Offset(x) for x in rationals]
        assert 0 < len(rationals)

        intervals = [self]
        new_intervals = []
        for rational in sorted(rationals):
            for interval in intervals:
                if interval.start_offset < rational < interval.stop_offset:
                    new_intervals.append(
                        type(self)(interval.start_offset, rational, self))
                    new_intervals.append(
                        type(self)(rational, interval.stop_offset, self))
                else:
                    new_intervals.append(type(self)(interval))
            intervals = new_intervals
            new_intervals = []

        return tuple(sorted(intervals, key=lambda x: x.signature))
