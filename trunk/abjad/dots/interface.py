from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface

#class _DotsInterface(_Interface):
class _DotsInterface(_Interface, _AttributeFormatter):

   def __init__(self, client):
      #_Interface.__init__(self, client, 'Dots', [ ])
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'Dots')
