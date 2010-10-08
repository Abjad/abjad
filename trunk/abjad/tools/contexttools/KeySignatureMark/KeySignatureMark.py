from abjad.tools.contexttools.Mark import Mark


class KeySignatureMark(Mark):
   '''.. versionadded:: 1.1.2
   
   The Abjad model of a key signature setting or key signature change.
   '''

   #__slots__ = ('_tonic', '_mode')

   _format_slot = 'opening'

   def __init__(self, tonic, mode, target_context = None):
      from abjad.components import Staff
      from abjad.tools import pitchtools
      from abjad.tools import tonalitytools
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      tonic = pitchtools.NamedChromaticPitchClass(tonic)
      mode = tonalitytools.Mode(mode)
      #object.__setattr__(self, '_tonic', tonic)
      #object.__setattr__(self, '_mode', mode)
      self._tonic = tonic
      self._mode = mode
      self._contents_repr_string = "'%s', '%s'" % (tonic, mode)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.tonic == arg.tonic:
            if self.mode == arg.mode:
               return True
      return False

   def __str__(self):
      return '%s-%s' % (self.tonic, self.mode)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\key %s \%s' % (self.tonic, self.mode)

   @property
   def mode(self):
      '''Read-only mode.'''
      return self._mode

   @property
   def name(self):
      if self.mode.mode_name_string == 'major':
         tonic = self.tonic.name.upper( )   
      else:
         tonic = self.tonic.name
      return '%s %s' % (tonic, self.mode.mode_name_string)

   @property
   def tonic(self):
      '''Read-only tonic.'''
      return self._tonic
