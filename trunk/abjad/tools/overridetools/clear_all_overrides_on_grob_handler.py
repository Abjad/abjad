from abjad.core import _GrobHandler


def clear_all_overrides_on_grob_handler(grob_handler):
   '''Clear all composer-defined attributes on AccidentalInterface,
   BeamInterface, DotsInterface, etc.

   NOW DEPRECATED. DO NOT USE.

   .. versionchanged:: 1.1.2
      renamed ``overridetools.clear_all( )`` to
      ``overridetools.clear_all_overrides_on_grob_handler( )``.
   '''

   raise Exception('DEPRECATED: DO NOT USE.')

   assert isinstance(grob_handler, _GrobHandler)

   for key, value in vars(grob_handler).items( ):
      if not key.startswith('_'):
         delattr(grob_handler, key)
