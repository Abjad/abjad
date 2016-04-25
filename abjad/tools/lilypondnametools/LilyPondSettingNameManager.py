# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondSettingNameManager(LilyPondNameManager):
    '''LilyPond setting name manager.
    '''

    ### CLASS VARIABLES ###

    skeleton_string_prefix = 'set__'

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        r'''Gets setting `name` from LilyPond setting name manager.

        Returns string.
        '''
        from abjad import ly
        from abjad.tools import lilypondnametools
        camel_name = stringtools.to_upper_camel_case(name)
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)
        elif camel_name in ly.contexts:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = lilypondnametools.LilyPondNameManager()
                vars(self)['_' + name] = context
                return context
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        from abjad.tools import lilypondnametools
        result = []
        for name, value in vars(self).items():
            if type(value) is lilypondnametools.LilyPondNameManager:
                prefixed_context_name = name
                context_name = prefixed_context_name.strip('_')
                context_proxy = value
                attribute_pairs = context_proxy._get_attribute_pairs()
                for attribute_name, attribute_value in attribute_pairs:
                    triple = (context_name, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name, attribute_value = name, value
                result.append((attribute_name, attribute_value))
        return result

    def _get_skeleton_strings(self):
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 2:
                attribute_name, attribute_value = attribute_tuple
                string = '{}={}'.format(attribute_name, repr(attribute_value))
                result.append(string)
            elif len(attribute_tuple) == 3:
                context_name, attribute_name, attribute_value = attribute_tuple
                key = '__'.join((context_name, attribute_name))
                string = '{}={}'.format(key, repr(attribute_value))
                result.append(string)
            else:
                message = 'attribute tuple must have length 2 or 3.'
                raise ValueError(message)
        result = ['set__' + x for x in result]
        return result
