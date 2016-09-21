# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class Block(AbjadObject):
    '''A LilyPond file block.

    ..  container:: example

        ::

            >>> block = lilypondfiletools.Block(name='paper')
            >>> block.left_margin = lilypondfiletools.LilyPondDimension(2, 'cm')
            >>> block.right_margin = lilypondfiletools.LilyPondDimension(2, 'cm')
            >>> block
            <Block(name='paper')>

        ::

            >>> print(format(block))
            \paper {
                left-margin = 2\cm
                right-margin = 2\cm
            }

    ..  container:: example

        ::

            >>> block = lilypondfiletools.Block(name='score')
            >>> markup = Markup('foo')
            >>> block.items.append(markup)
            >>> block
            <Block(name='score')>

        ::

            >>> print(format(block))
            \score {
                {
                    \markup { foo }
                }
            }

    '''

    ### INITIALIZER ###

    def __init__(self, name='score'):
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
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getitem__(self, name):
        r'''Gets block item with `name`.

        ..  container:: example

            Gets score with name ``'Red Example Score'`` in score block:

            ::

                >>> block = lilypondfiletools.Block(name='score')
                >>> score = Score(name='Red Example Score')
                >>> block.items.append(score)

            ::

                >>> block['Red Example Score']
                Score(is_simultaneous=True)

        Raises key error when no item with `name` is found.
        '''
        for item in self.items:
            if getattr(item, 'name', None) == name:
                return item
        raise KeyError

    ### PRIVATE METHODS ###

    def _format_item(self, item, depth=1):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent * depth
        result = []
        if isinstance(item, (list, tuple)):
            result.append(indent + '{')
            for x in item:
                result.extend(self._format_item(x, depth + 1))
            result.append(indent + '}')
        elif isinstance(item, str):
            string = indent + item
            result.append(string)
        elif '_get_format_pieces' in dir(item):
            pieces = item._get_format_pieces()
            pieces = (indent + item for item in pieces)
            result.extend(pieces)
        return result

    def _get_format_pieces(self):
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        result = []
        if not self._get_formatted_user_attributes() and \
            not getattr(self, 'contexts', None) and \
            not getattr(self, 'context_blocks', None) and \
            not len(self.items):
            if self.name == 'score':
                return ''
            string = '{} {{}}'.format(self._escaped_name)
            result.append(string)
            return result
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        prototype = (scoretools.Leaf, markuptools.Markup)
        for item in self.items:
            if isinstance(item, lilypondfiletools.ContextBlock):
                continue
            if isinstance(item, prototype):
                item = [item]
            result.extend(self._format_item(item))
        formatted_attributes = self._get_formatted_user_attributes()
        formatted_attributes = [indent + x for x in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = getattr(
            self, '_formatted_context_blocks', [])
        formatted_context_blocks = [indent + x for x in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        result.append('}')
        return result

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_bracketed=True,
            repr_is_indented=False,
            )

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

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_context_blocks(self):
        from abjad.tools import lilypondfiletools
        result = []
        context_blocks = []
        for item in self.items:
            if isinstance(item, lilypondfiletools.ContextBlock):
                context_blocks.append(item)
        for context_block in context_blocks:
            result.extend(context_block._get_format_pieces())
        return result

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _user_attributes(self):
        all_attributes = list(vars(self).keys())
        user_attributes = [x for x in all_attributes if not x.startswith('_')]
        user_attributes.sort()
        return user_attributes

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items in block.

        ..  container:: example

            ::

                >>> block = lilypondfiletools.Block(name='score')
                >>> markup = Markup('foo')
                >>> block.items.append(markup)

            ::

                >>> block.items
                [Markup(contents=('foo',))]

        Returns list.
        '''
        return self._items

    @property
    def name(self):
        r'''Gets name of block.

        ..  container:: example

            ::

                >>> block = lilypondfiletools.Block(name='score')
                >>> markup = Markup('foo')
                >>> block.items.append(markup)

            ::

                >>> block.name
                'score'

        Returns string.
        '''
        return self._name
