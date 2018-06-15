from abjad.system.AbjadObject import AbjadObject
from abjad.system.LilyPondFormatManager import \
    LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager


class Block(AbjadObject):
    """
    A LilyPond file block.

    ..  container:: example

        REGRESSION. Blocks remember attribute assignment order.

        Here right margin precedes left margin even though left margin
        alphabetizes before right margin:

        >>> block = abjad.Block(name='paper')
        >>> block.right_margin = abjad.LilyPondDimension(2, 'cm')
        >>> block.left_margin = abjad.LilyPondDimension(2, 'cm')
        >>> block
        <Block(name='paper')>

        >>> abjad.f(block)
        \paper {
            right-margin = 2\cm
            left-margin = 2\cm
        }

    ..  container:: example

        >>> block = abjad.Block(name='score')
        >>> markup = abjad.Markup('foo')
        >>> block.items.append(markup)
        >>> block
        <Block(name='score')>

        >>> abjad.f(block)
        \score {
            {
                \markup { foo }
            }
        }

    """

    ### INITIALIZER ###

    def __init__(self, name='score'):
        assert isinstance(name, str), repr(name)
        self._name = name
        escaped_name = rf'\{name}'
        self._escaped_name = escaped_name
        self._items = []
        self._public_attribute_names = []

    ### SPECIAL METHODS ###

    def __delattr__(self, name) -> None:
        """
        Deletes block attribute with ``name``.

        ..  container:: example

            >>> header_block = abjad.Block(name='header')
            >>> header_block.tagline = False
            >>> header_block.tagline
            False

            >>> delattr(header_block, 'tagline')
            >>> hasattr(header_block, 'tagline')
            False

        """
        self._public_attribute_names.remove(name)
        object.__delattr__(self, name)

    def __format__(self, format_specification=''):
        """
        Formats block.

        Returns string.
        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        else:
            assert format_specification == 'storage'
            return StorageFormatManager(self).get_storage_format()

    def __getitem__(self, name):
        """
        Gets item with ``name``.

        ..  container:: example

            Gets score with name ``'Red Example Score'`` in score block:

            >>> block = abjad.Block(name='score')
            >>> score = abjad.Score(name='Red Example Score')
            >>> block.items.append(score)

            >>> block['Red Example Score']
            Score(is_simultaneous=True, name='Red Example Score')

        Returns item.

        Raises key error when no item with ``name`` is found.
        """
        for item in self.items:
            if getattr(item, 'name', None) == name:
                return item
        raise KeyError

    def __setattr__(self, name, value):
        """
        Sets block ``name`` to ``value``.

        Returns none.
        """
        if (
            not name.startswith('_') and
            name not in self._public_attribute_names
            ):
            self._public_attribute_names.append(name)
        object.__setattr__(self, name, value)

    def __setstate__(self, state):
        """
        Sets state of block.

        Returns none.
        """
        if not hasattr(self, '_public_attribute_names'):
            self._public_attribute_names = []
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_context_blocks(self):
        import abjad
        result = []
        context_blocks = []
        for item in self.items:
            if isinstance(item, abjad.ContextBlock):
                context_blocks.append(item)
        for context_block in context_blocks:
            result.extend(context_block._get_format_pieces())
        return result

    ### PRIVATE METHODS ###

    def _format_item(self, item, depth=1):
        indent = LilyPondFormatManager.indent * depth
        result = []
        if isinstance(item, (list, tuple)):
            result.append(indent + '{')
            depth_ = depth + 1
            for x in item:
                pieces = self._format_item(x, depth=depth_)
                result.extend(pieces)
            result.append(indent + '}')
        elif isinstance(item, str):
            string = indent + item
            result.append(string)
        elif '_get_format_pieces' in dir(item):
            try:
                pieces = item._get_format_pieces()
            except TypeError:
                pieces = item._get_format_pieces()
            pieces = (indent + item for item in pieces)
            result.extend(pieces)
        return result

    def _get_format_pieces(self):
        import abjad
        indent = LilyPondFormatManager.indent
        result = []
        if (not self._get_formatted_user_attributes() and
            not getattr(self, 'contexts', None) and
            not getattr(self, 'context_blocks', None) and
            not len(self.items)):
            if self.name == 'score':
                return ''
            string = '{} {{}}'.format(self._escaped_name)
            result.append(string)
            return result
        string = '{} {{'.format(self._escaped_name)
        result.append(string)
        for item in self.items:
            if isinstance(item, abjad.ContextBlock):
                continue
            if isinstance(item, (abjad.Leaf, abjad.Markup)):
                item = [item]
            result.extend(self._format_item(item))
        formatted_attributes = self._get_formatted_user_attributes()
        formatted_attributes = [indent + _ for _ in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = getattr(
            self, '_formatted_context_blocks', [])
        formatted_context_blocks = [
            indent + _ for _ in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        result.append('}')
        return result

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            repr_is_bracketed=True,
            repr_is_indented=False,
            )

    def _get_formatted_user_attributes(self):
        import abjad
        result = []
        #prototype = (abjad.Scheme, abjad.LilyPondLiteral)
        prototype = abjad.Scheme
        for value in self.items:
            if isinstance(value, prototype):
                result.append(format(value, 'lilypond'))
        prototype = (
            abjad.Scheme,
            abjad.LilyPondDimension,
            #abjad.LilyPondLiteral,
            )
        for key in self._public_attribute_names:
            assert not key.startswith('_'), repr(key)
            value = getattr(self, key)
            # format subkeys via double underscore
            formatted_key = key.split('__')
            for i, k in enumerate(formatted_key):
                formatted_key[i] = k.replace('_', '-')
                if 0 < i:
                    string = "#'{}".format(formatted_key[i])
                    formatted_key[i] = string
            formatted_key = ' '.join(formatted_key)
            # format value
            if isinstance(value, abjad.Markup):
                formatted_value = value._get_format_pieces()
            elif isinstance(value, prototype):
                formatted_value = [format(value, 'lilypond')]
            else:
                formatted_value = abjad.Scheme(value)
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

    def _get_lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r"""
        Gets items in block.

        ..  container:: example

            >>> block = abjad.Block(name='score')
            >>> markup = abjad.Markup('foo')
            >>> block.items.append(markup)

            >>> block.items
            [Markup(contents=['foo'])]

        ..  container:: example

            Accepts strings:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> score_block = abjad.Block(name='score')
            >>> score_block.items.append('<<')
            >>> score_block.items.append(r'{ \include "layout.ly" }')
            >>> score_block.items.append(staff)
            >>> score_block.items.append('>>')
            >>> lilypond_file = abjad.LilyPondFile(
            ...     lilypond_language_token=False,
            ...     lilypond_version_token=False,
            ...     )
            >>> lilypond_file.items.append(score_block)

            >>> abjad.f(lilypond_file)
            \score {
                <<
                { \include "layout.ly" }
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
                >>
            }

        Returns list.
        """
        return self._items

    @property
    def name(self):
        """
        Gets name of block.

        ..  container:: example

            >>> block = abjad.Block(name='score')
            >>> markup = abjad.Markup('foo')
            >>> block.items.append(markup)

            >>> block.name
            'score'

        Returns string.
        """
        return self._name

    ### PUBLIC METHODS ###

    def empty(self):
        """
        Is true when block contains no items and has no user attributes.

        Returns true or false.
        """
        if not self.items and not self._get_formatted_user_attributes():
            return True
        return False
