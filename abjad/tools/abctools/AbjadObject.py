# -*- coding: utf-8 -*-
import abc


AbstractBase = abc.ABCMeta(
    'AbstractBase',
    (),
    {
        '__metaclass__': abc.ABCMeta,
        '__module__': __name__,
        '__slots__': (),
        },
    )


class AbjadObject(AbstractBase):
    '''Abstract base class from which many custom classes inherit.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when ID of `expr` equals ID of Abjad object.
        Otherwise false.

        Returns true or false.
        '''
        return id(self) == id(expr)

    def __format__(self, format_specification=''):
        r'''Formats Abjad object.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getstate__(self):
        r'''Gets state of Abjad object.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self):
        r'''Hashes Abjad object.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(AbjadObject, self).__hash__()

    def __ne__(self, expr):
        r'''Is true when Abjad object does not equal `expr`.
        Otherwise false.

        Returns true or false.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of Abjad object.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatAgent(self).get_repr_format()

    def __setstate__(self, state):
        r'''Sets state of Abjad object.

        Returns none.
        '''
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None, blank=False):
        if annotation is None:
            print('debug: {!r}'.format(value))
        else:
            print('debug ({}): {!r}'.format(annotation, value))
        if blank:
            print()

    def _debug_values(self, values, annotation=None, blank=True):
        if values:
            for value in values:
                self._debug(value, annotation=annotation)
            if blank:
                print()
        else:
            self._debug(repr(values), annotation=annotation)
            if blank:
                print()

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(client=self)

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menu_summary(self):
        return str(self)
