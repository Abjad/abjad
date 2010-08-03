from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces._Interface import _Interface


class DotsInterface(_Interface, _GrobHandler):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Dots')
