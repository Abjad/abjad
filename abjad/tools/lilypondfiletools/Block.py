# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Block(AbjadObject):
    '''A LilyPond file block.

    ..  container:: example

        ::

            >>> block = lilypondfiletools.Block(name='paper')
            >>> block.left_margin = lilypondfiletools.LilyPondDimension(2, 'cm')
            >>> block.right_margin = lilypondfiletools.LilyPondDimension(2, 'cm')

        ::

            >>> print format(block)
            \paper {
                left-margin = 2\cm
                right-margin = 2\cm
            }

    '''

    ### INITIALIZER ###

    def __init__(self, name=None):
        assert isinstance(name, str), repr(name)
        self._name = name
        escaped_name = r'\{}'.format(name)
        self._escaped_name = escaped_name
        self._items = []

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats block.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        result = []
        if not self._get_formatted_user_attributes() and \
            not getattr(self, 'contexts', None) and \
            not getattr(self, 'context_blocks', None) and \
            not len(self.items):
            string = '{} {{}}'.format(self._escaped_name)
            result.append(string)
            return result
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        prototype = (scoretools.Leaf, markuptools.Markup)
        if len(self.items) == 1 and isinstance(self.items[0], prototype):
            result.append('\t{')
            pieces = self.items[0]._format_pieces
            pieces = ['\t\t' + item for item in pieces]
            result.extend(pieces)
            result.append('\t}')
            return result
        for item in self.items:
            if isinstance(item, str):
                string = '\t{}'.format(item)
                result.append(string)
            elif hasattr(item, '_get_format_pieces'):
                pieces = item._get_format_pieces()
                pieces = ['\t' + item for item in pieces]
                result.extend(pieces)
            elif hasattr(item, '_format_pieces'):
                pieces = item._format_pieces
                pieces = ['\t' + item for item in pieces]
                result.extend(pieces)
            else:
                pass
        formatted_attributes = self._get_formatted_user_attributes()
        formatted_attributes = ['\t' + x for x in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = getattr(
            self, '_formatted_context_blocks', [])
        formatted_context_blocks = ['\t' + x for x in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        result.append('}')
        return result

    @property
    def _lilypond_format(self):
        return '\n'.join(self._format_pieces)

    @property
    def _user_attributes(self):
        all_attributes = vars(self).keys()
        user_attributes = [x for x in all_attributes if not x.startswith('_')]
        user_attributes.sort()
        return user_attributes

    ### PRIVATE METHODS ###

    def _get_formatted_user_attributes(self):
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import schemetools
        result = []
        for value in self.items:
            acceptable_types = (
                schemetools.Scheme, 
                indicatortools.LilyPondCommand,
                )
            if isinstance(value, acceptable_types):
                result.append(format(value, 'lilypond'))
        for key, value in sorted(vars(self).items()):
            if not key.startswith('_'):
                # format subkeys via double underscore
                formatted_key = key.split('__')
                for i, k in enumerate(formatted_key):
                    formatted_key[i] = k.replace('_', '-')
                    if 0 < i:
                        string = "#'{}".format(formatted_key[i])
                        formatted_key[i] = string
                formatted_key = ' '.join(formatted_key)
                # format value
                accetable_types = (
                    schemetools.Scheme,
                    lilypondfiletools.LilyPondDimension,
                    indicatortools.LilyPondCommand,
                    )
                if isinstance(value, markuptools.Markup):
                    formatted_value = value._get_format_pieces()
                elif isinstance(value, accetable_types):
                    formatted_value = [format(value, 'lilypond')]
                else:
                    formatted_value = schemetools.Scheme(value)
                    formatted_value = format(formatted_value, 'lilypond')
                    formatted_value = [formatted_value]
                setting = '{!s} = {!s}'
                setting = setting.format(
                    formatted_key, 
                    formatted_value[0],
                    )
                result.append(setting)
                result.extend(formatted_value[1:])
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items in block.

        ..  container:: example

            ::

                >>> block.items
                []

        Returns list.
        '''
        return self._items

    @property
    def name(self):
        r'''Gets name of block.

        ..  container:: example

            ::

                >>> block.name
                'paper'

        Returns string.
        '''
        return self._name
