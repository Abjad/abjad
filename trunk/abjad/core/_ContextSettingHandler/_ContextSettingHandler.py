from abjad.core._Abjad import _Abjad
from abjad.core._Parser import _Parser


class _ContextSettingHandler(_Abjad):
   '''Abstract mix-in base class to identify *Abjad* classes
      that handle one or more *LilyPond* context settings.
      Concrete classes that inherit from ``_ContextSettingHandler``
      get picked up at format-time and asked for format contributions.'''

   def __init__(self):
      self._parser = _Parser( )
      self._promotions = { }

   ## PRIVATE METHODS ##

   def _promoted_setting(self, setting):
      context = self._promotions.get(setting, None)
      if context is not None:
         return '%s.%s' % (str(context), setting)
      else:
         return setting

   ## PUBLIC ATTRIBUTES ##

   @property
   def settings(self):
      '''List of *LilyPond* context settings.
         Override in concrete child classes.'''
      result = [ ]
      return result

   ## PUBLIC METHODS ##

   def promote_attribute_to_context_on_grob_handler(self, setting, context):
      '''Promote ``setting`` to *LilyPond* ``context``.'''
      assert isinstance(context, str)
      if hasattr(self, setting):
         self._promotions[setting] = context
      else:
         raise AttributeError('no %s context setting.' % setting)
