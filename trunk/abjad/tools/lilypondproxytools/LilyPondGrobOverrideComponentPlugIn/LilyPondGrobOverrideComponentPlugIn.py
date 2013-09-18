# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondproxytools.LilyPondGrobProxy import LilyPondGrobProxy
from abjad.tools.lilypondproxytools.LilyPondGrobProxyContextWrapper \
	import LilyPondGrobProxyContextWrapper
from abjad.tools.lilypondproxytools.LilyPondComponentPlugIn \
	import LilyPondComponentPlugIn


class LilyPondGrobOverrideComponentPlugIn(LilyPondComponentPlugIn):
    '''LilyPond grob override component plug-in.
    '''

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        from abjad import ly
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                message = '"%s" object has no attribute: "%s".'
                raise AttributeError(message % (self.__class__.__name__, name))
        else:
            camel_name = stringtools.snake_case_to_upper_camel_case(name)
            if camel_name in ly.contexts:
                try:
                    return vars(self)['_' + name]
                except KeyError:
                    context = LilyPondGrobProxyContextWrapper()
                    vars(self)['_' + name] = context
                    return context
            elif camel_name in ly.grob_interfaces:
                try:
                    return vars(self)[name]
                except KeyError:
                    vars(self)[name] = LilyPondGrobProxy()
                    return vars(self)[name]
            else:
                return vars(self)[name]

    def __repr__(self):
        body_string = ''
        skeleton_strings = self._get_skeleton_strings()
        if skeleton_strings:
            # remove 'override__'
            skeleton_strings = [x[10:] for x in skeleton_strings]
            skeleton_strings.sort()
            body_string = ', '.join(skeleton_strings)
        return '%s(%s)' % (self.__class__.__name__, body_string)

    def __setattr__(self, attr, value):
        # make sure attr is valid grob name before setting value
        attr_value = getattr(self, attr)
        object.__setattr__(self, attr, value)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).iteritems():
            if isinstance(value, LilyPondGrobProxy):
                grob_name, grob_proxy = name, value
                for attribute_name, attribute_value in \
                    vars(grob_proxy).iteritems():
                    result.append(
                        (grob_name, attribute_name, attribute_value))
            else:
                context_name, context_proxy = name.strip('_'), value
                for grob_name, grob_proxy in vars(context_proxy).iteritems():
                    for attribute_name, attribute_value in \
                        vars(grob_proxy).iteritems():
                        result.append((
                            context_name, 
                            grob_name, 
                            attribute_name, 
                            attribute_value,
                            ))
        return tuple(result)

    def _get_skeleton_strings(self):
        skeleton_strings = []
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            value = getattr(
                value, '_tools_package_qualified_repr', repr(value))
            skeleton_string = 'override__{}={}'.format(most, value)
            skeleton_strings.append(skeleton_string)
        return tuple(skeleton_strings)

    def _list_format_contributions(self, contribution_type, is_once=False):
        from abjad.tools import formattools
        assert contribution_type in ('override', 'revert')
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context_name = None
                grob_name = attribute_tuple[0]
                attribute_name = attribute_tuple[1]
                attribute_value = attribute_tuple[2]
            elif len(attribute_tuple) == 4:
                context_name = attribute_tuple[0]
                grob_name = attribute_tuple[1]
                attribute_name = attribute_tuple[2]
                attribute_value = attribute_tuple[3]
            else:
                raise ValueError
            if contribution_type == 'override':
                override_string = formattools.make_lilypond_override_string(
                    grob_name, 
                    attribute_name,
                    attribute_value, 
                    context_name=context_name, 
                    is_once=is_once,
                    )
                result.append(override_string)
            else:
                revert_string = formattools.make_lilypond_revert_string(
                    grob_name, 
                    attribute_name, 
                    context_name=context_name,
                    )
                result.append(revert_string)
        result.sort()
        return result

    def _make_override_dictionary(self):
        result = {}
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            attribute = '_tools_package_qualified_repr'
            value = getattr(value, attribute, repr(value))
            result[most] = value 
        return result
