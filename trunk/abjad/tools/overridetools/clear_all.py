from abjad.core.grobhandler import _GrobHandler


def clear_all(grob_handler):
   '''Clear all composer-defined attributes on AccidentalInterface,
   BeamInterface, DotsInterface, etc.
   '''

   assert isinstance(grob_handler, _GrobHandler)

   for key, value in vars(grob_handler).items( ):
      if not key.startswith('_'):
         delattr(grob_handler, key)
