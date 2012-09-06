import abc


class AttributedBlock(object):
    '''.. versionadded:: 2.0

    Abjad model of LilyPond input file block with attributes.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._is_formatted_when_empty = False

    ### SPECIAL METHODS ###

    def __repr__(self):
        if not len(self._user_attributes):
            return '%s()' % type(self).__name__
        else:
            return '%s(%s)' % (type(self).__name__, len(self._user_attributes))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        result = []
        if not self._formatted_user_attributes and not getattr(self, 'contexts', None) \
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
        formatted_context_blocks = getattr(self, '_formatted_context_blocks', [])
        formatted_context_blocks = ['\t' + line for line in formatted_context_blocks]
        result.extend(formatted_context_blocks)
        result.append('}')
        return result

    @property
    def _formatted_user_attributes(self):
        from abjad.tools import markuptools
        from abjad.tools import schemetools
        result = []
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
                if isinstance(value, markuptools.Markup):
                    formatted_value = value.lilypond_format
                elif isinstance(value, schemetools.Scheme):
                    formatted_value = value.lilypond_format
                else:
                    formatted_value = schemetools.Scheme(value).lilypond_format
                setting = '%s = %s' % (formatted_key, formatted_value)
                result.append(setting)
        return result

    @property
    def _user_attributes(self):
        all_attributes = vars(self).keys()
        user_attributes = [x for x in all_attributes if not x.startswith('_')]
        user_attributes.sort()
        return user_attributes

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        return '\n'.join(self._format_pieces)

    @apply
    def is_formatted_when_empty():
        def fget(self):
            return self._is_formatted_when_empty
        def fset(self, arg):
            if isinstance(arg, bool):
                self._is_formatted_when_empty = arg
            else:
                raise TypeError
        return property(**locals())
