from abjad.core.LilyPondContextProxy.LilyPondContextProxy import LilyPondContextProxy
from abjad.core._LilyPondComponentPlugIn import _LilyPondComponentPlugIn


class LilyPondContextSettingComponentPlugIn(_LilyPondComponentPlugIn):
    '''.. versionadded:: 2.0

    LilyPond context setting namespace.
    '''

    _known_lilypond_contexts = set([
        'choir_staff', 'chord_names', 'cue_voice', 'devnull', 'drum_staff',
        'drum_voice', 'dynamics', 'figured_bass', 'fret_boards', 'global',
        'grand_staff', 'gregorian_transcription_staff', 'gregorian_transcription_voice',
        'lyrics', 'mensural_staff', 'mensural_voice', 'note_names', 'piano_staff',
        'rhythmic_staff', 'score', 'staff', 'staff_group', 'tab_staff',
        'tab_voice', 'vaticana_staff', 'vaticana_voice', 'voice'])

    ### OVERLOADS ###

    def __getattr__(self, name):
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                raise AttributeError('"%s" object has no attribute: "%s".' % (
                    self.__class__.__name__, name))
        elif name in type(self)._known_lilypond_contexts:
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

    def _get_skeleton_strings(self):
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 2:
                attribute_name, attribute_value = attribute_tuple
                result.append('%s = %s' % (attribute_name, repr(attribute_value)))
            elif len(attribute_tuple) == 3:
                context_name, attribute_name, attribute_value = attribute_tuple
                key = '__'.join((context_name, attribute_name))
                result.append('%s = %s' % (key, repr(attribute_value)))
            else:
                raise ValueError
        result = ['set__' + x for x in result]
        return result

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
