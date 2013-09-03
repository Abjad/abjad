# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Interval(AbjadObject):
    '''Interval base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ('_format_string', )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        raise NotImplementedError(
            'abs needs to be implemented on %s.' % type(self))

    def __float__(self):
        raise NotImplementedError(
            'float needs to be implemented on %s.' % type(self))

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError(
            'int needs to be implemented on %s.' % type(self))

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return str(self.number)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        return 100 * self.semitones

    # TODO: remove
    @property
    def interval_class(self):
        pass

    # TODO: remove
    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        pass
