from abjad.core.grobhandler import _GrobHandler


class KeySignature(_GrobHandler):

   def __init__(self, pitch_class_letter, mode):
      _GrobHandler.__init__(self, 'KeySignature')
      self.pitch_class_letter = pitch_class_letter
      self.mode = mode

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, KeySignature):
         if self.pitch_class_letter == arg.pitch_class_letter:
            if self.mode == arg.mode:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return 'KeySignature(%s, %s)' % (self.pitch_class_letter, self.mode)

   def __str__(self):
      return '%s-%s' % (self.pitch_class_letter, self.mode)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\key %s \%s' % (self.pitch_class_letter, self.mode)

   @apply
   def mode( ):
      def fget(self):
         return self._mode
      def fset(self, arg):
         if not isinstance(arg, str):
            raise TypeError('must be str.')
         self._mode = arg
      return property(**locals( ))

   @apply
   def pitch_class_letter( ):
      def fget(self):
         return self._pitch_class_letter
      def fset(self, arg):
         if not isinstance(arg, str):
            raise TypeError('must be str.')
         self._pitch_class_letter = arg
      return property(**locals( ))
