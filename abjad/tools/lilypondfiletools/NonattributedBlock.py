# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class NonattributedBlock(AbjadObject):
    r'''Abjad model of LilyPond input file block with no attributes.
    '''

    ### INITIALIZER ###

    def __init__(self):
        self._items = []

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats nonattributed block.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of nonattributed block.

        Returns string.
        '''
        if not len(self.items):
            return '{}()'.format(type(self).__name__)
        else:
            return '{}({})'.format(type(self).__name__, len(self.items))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        if not len(self.items):
            result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            for x in self.items:
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
    def items(self):
        r'''Gets items in nonattributed block.

        Returns list.
        '''
        return self._items
