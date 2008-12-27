from abjad.core.formatter import _Formatter


class _ContainerFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self.opening = [ ]
      self.closing = [ ]

   ### PRIVATE ATTRIBUTES ###

   @property
   def _contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result
   
   @property
   def _invocation_closing(self):
      result = [ ]
      close = self._client.brackets.close
      if close != ')':
         result.append(close)
      return result

   @property
   def _invocation_opening(self):
      result = [ ]
      open = self._client.brackets.open
      if open != '(':
         result.append(open)
      return result

   @property
   def _opening(self):
      result = [ ]
      accidentals = self._client.accidentals
      if accidentals:
         result.append(r"#(set-accidental-style '%s)" % accidentals)
      result.extend(self._collectLocation('_opening'))
      return ['\t' + x for x in result]

   ### PUBLIC ATTRIBUTES ###

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      ### TODO: shouldn't the following line be here? and for _after as well?
      # result.extend(self._collectLocation('_before'))
      result.extend(self._invocation_opening)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      ### TODO: this line needs to be replaced with the one below;
      ###       we should discuss [TB 2008-12-03]
      #result.extend(self._closing)
      result.extend(self._collectLocation('_closing'))
      result.extend(self.closing)
      result.extend(self._invocation_closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
