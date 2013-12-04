# -*- encoding: utf-8 -*-
import abc
import types


class AbjadObject(object):
    '''Abstract base class from which all custom classes should inherit.

    Abjad objects compare equal only with equal object IDs.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when ID of `expr` equals ID of Abjad object.

        Returns boolean.
        '''
        return id(self) == id(expr)

    def __format__(self, format_specification=''):
        r'''Formats object.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getstate__(self):
        r'''Gets object state.
        '''
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __ne__(self, expr):
        r'''True when ID of `expr` does not equal ID of Abjad object.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Interpreter representation of Abjad object.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    def __setstate__(self, state):
        r'''Sets object state.
        '''
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return str(self)

    @property
    def _repr_specification(self):
        return self._storage_format_specification.__makenew__(
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(self)

    ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None, blank=False):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)
        if blank:
            print ''

    def _debug_values(self, values, annotation=None, blank=True):
        if values:
            for value in values:
                self._debug(value, annotation=annotation)
            if blank:
                print ''
        else:
            self._debug(repr(values), annotation=annotation)
            if blank:
                print ''
