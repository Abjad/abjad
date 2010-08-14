class LilyPondContextNamespace(object):
   '''.. versionadded:: 1.1.2

   LilyPond context namespace.
   '''

   def __init__(self, lilypond_context):
      self._lilypond_context = lilypond_context

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._lilypond_context)
