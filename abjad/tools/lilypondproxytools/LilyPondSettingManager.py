# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondObjectProxy \
    import LilyPondObjectProxy


class LilyPondSettingManager(LilyPondObjectProxy):
    '''LilyPond setting manager.
    '''

    ### CLASS VARIABLES ###

    skeleton_string_prefix = 'set__'

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        from abjad import ly
        from abjad.tools import lilypondproxytools
        camel_name = stringtools.snake_case_to_upper_camel_case(name)
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
                context = lilypondproxytools.LilyPondObjectProxy()
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
        from abjad.tools import lilypondproxytools
        result = []
        for name, value in vars(self).iteritems():
            if type(value) is lilypondproxytools.LilyPondObjectProxy:
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
