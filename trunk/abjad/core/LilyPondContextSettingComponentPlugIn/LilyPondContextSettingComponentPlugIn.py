from abjad.core.LilyPondContextProxy.LilyPondContextProxy import LilyPondContextProxy


class LilyPondContextSettingComponentPlugIn(object):
   '''.. versionadded:: 1.1.2

   LilyPond context setting namespace.
   '''

   def __init__(self):
      pass

   _known_lilypond_contexts = set([
      'choir_staff', 'chord_names', 'cue_voice', 'devnull', 'drum_staff', 
      'drum_voice', 'dynamics', 'figured_bass', 'fret_boards', 'global', 
      'grand_staff', 'gregorian_transcription_staff', 'gregorian_transcription_voice', 
      'lyrics', 'mensural_staff', 'mensural_voice', 'note_names', 'piano_staff', 
      'rhythmic_staff', 'score', 'staff', 'staff_group', 'tab_staff', 
      'tab_voice', 'vaticana_staff', 'vaticana_voice', 'voice'])

   ## OVERLOADS ##

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
            context = LilyPondContextProxy( )
            vars(self)['_' + name] = context
            return context
      else:
         try:
            return vars(self)[name]
         except KeyError:
            raise AttributeError('"%s" object has no attribute: "%s".' % (
               self.__class__.__name__, name))

   def __repr__(self):
      return '%s( )' % self.__class__.__name__
