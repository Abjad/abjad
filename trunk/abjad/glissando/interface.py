from .. core.interface import _Interface

class GlissandoInterface(_Interface):

   def __init__(self, leaf, start = False, thickness = False, style = False):
      self._leaf = leaf
      self._start = start
      self._thickness = thickness
      self._style = style

   def clear(self):
      self._start = False
      self._thickness = False
      self._style = False

   def __repr__(self):
      if self._start:
         return 'Glissando(+)'
      else:
         return 'Glissando( )'

   @property
   def before(self):
      result = []
      base = r'\once \override Glissando '
      if self._thickness and self._thickness != 'revert':
         result.append(base + "#'thickness = #%s" % self._thickness)
      if self._style and self._style != 'revert':
         result.append(base + "#'style = #'%s" % self._style)
      return result

   @property
   def after(self):
      result = []
      if self._thickness and self._thickness == 'revert':
         result.append(r"\revert Glissando #'thickness")
      if self._style and self._style == 'revert':
         result.append(r"\revert Glissando #'style")
      return result

   @property
   def right(self):
      if self._start:
         return [r'\glissando']
      else:
         return []
