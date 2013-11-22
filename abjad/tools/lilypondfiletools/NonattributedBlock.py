# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class NonattributedBlock(list, AbjadObject):
    r'''Abjad model of LilyPond input file block with no attributes.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        if not len(self):
            return '%s()' % type(self).__name__
        else:
            return '%s(%s)' % (type(self).__name__, len(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        if not len(self):
            if self._is_formatted_when_empty:
                result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            for x in self:
                if hasattr(x, '_format_pieces'):
                    result.extend(['\t' + piece for piece in x._format_pieces])
                elif isinstance(x, str):
                    result.append('\t%s' % x)
            result.append('}')
        return result

    @property
    def _lilypond_format(self):
        return '\n'.join(self._format_pieces)

    ### PUBLIC PROPERTIES ###

    @property
    def is_formatted_when_empty(self):
        return self._is_formatted_when_empty

    @is_formatted_when_empty.setter
    def is_formatted_when_empty(self, arg):
        if isinstance(arg, bool):
            self._is_formatted_when_empty = arg
        else:
            raise TypeError
