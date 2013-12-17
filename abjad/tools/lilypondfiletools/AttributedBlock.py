# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class AttributedBlock(list, AbjadObject):
    '''Abjad model of LilyPond input file block with attributes.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._is_formatted_when_empty = False

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats attributed block.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of attributed block.

        Returns string.
        '''
        if not len(self._user_attributes):
            return '{}()'.format(type(self).__name__)
        else:
            return '{}({})'.format(
                type(self).__name__, 
                len(self._user_attributes),
                )

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        if not self._formatted_user_attributes and \
            not getattr(self, 'contexts', None) \
            and not getattr(self, 'context_blocks', None):
            if self.is_formatted_when_empty:
                result.append('%s {}' % self._escaped_name)
                return result
            else:
                return result
        result.append('%s {' % self._escaped_name)
        if getattr(self, 'contexts', None):
            specs = self._formatted_context_specifications
            result.extend(['\t' + x for x in specs])
        formatted_attributes = self._formatted_user_attributes
        formatted_attributes = ['\t' + x for x in formatted_attributes]
        result.extend(formatted_attributes)
        formatted_context_blocks = getattr(
            self, '_formatted_context_blocks', [])
        formatted_context_blocks = [
            '\t' + line for line in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        result.append('}')
        return result

    @property
    def _formatted_user_attributes(self):
        from abjad.tools import lilypondfiletools
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import schemetools
        result = []
        for value in self:
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
                        formatted_key[i] = "#'%s" % formatted_key[i]
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

    @property
    def _lilypond_format(self):
        return '\n'.join(self._format_pieces)

    @property
    def _user_attributes(self):
        all_attributes = vars(self).keys()
        user_attributes = [x for x in all_attributes if not x.startswith('_')]
        user_attributes.sort()
        return user_attributes

    ### PUBLIC PROPERTIES ###

    @property
    def is_formatted_when_empty(self):
        r'''True when attributed block is formatted when empty. Otherwise
        false.

        Returns boolean.
        '''
        return self._is_formatted_when_empty

    @is_formatted_when_empty.setter
    def is_formatted_when_empty(self, arg):
        if isinstance(arg, bool):
            self._is_formatted_when_empty = arg
        else:
            raise TypeError
