from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondContextProxy.LilyPondContextProxy import LilyPondContextProxy
from abjad.tools.lilypondproxytools.LilyPondComponentPlugIn import LilyPondComponentPlugIn


class LilyPondContextSettingComponentPlugIn(LilyPondComponentPlugIn):
    '''.. versionadded:: 2.0

    LilyPond context setting namespace.
    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        from abjad import ly
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                raise AttributeError('"%s" object has no attribute: "%s".' % (
                    self.__class__.__name__, name))
        elif stringtools.underscore_delimited_lowercase_to_uppercamelcase(name) in ly.contexts:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = LilyPondContextProxy()
                vars(self)['_' + name] = context
                return context
        else:
            try:
                return vars(self)[name]
            except KeyError:
                raise AttributeError('"%s" object has no attribute: "%s".' % (
                    self.__class__.__name__, name))

    def __repr__(self):
        body_string = ' '
        skeleton_strings = self._get_skeleton_strings()
        if skeleton_strings:
            # remove 'set__'
            skeleton_strings = [x[5:] for x in skeleton_strings]
            body_string = ', '.join(skeleton_strings)
        return '%s(%s)' % (self.__class__.__name__, body_string)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).iteritems():
            if isinstance(value, LilyPondContextProxy):
                prefixed_context_name = name
                context_name = prefixed_context_name.strip('_')
                context_proxy = value
                for attribute_name, attribute_value in context_proxy._get_attribute_pairs():
                    result.append((context_name, attribute_name, attribute_value))
            else:
                attribute_name, attribute_value = name, value
                result.append((attribute_name, attribute_value))
        return result

    def _get_skeleton_strings(self):
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 2:
                attribute_name, attribute_value = attribute_tuple
                result.append('%s=%s' % (attribute_name, repr(attribute_value)))
            elif len(attribute_tuple) == 3:
                context_name, attribute_name, attribute_value = attribute_tuple
                key = '__'.join((context_name, attribute_name))
                result.append('%s=%s' % (key, repr(attribute_value)))
            else:
                raise ValueError
        result = ['set__' + x for x in result]
        return result
