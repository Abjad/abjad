from abjad.components._Leaf import _Leaf


def _get_mark_format_contributions_for_slot(leaf, slot):
   from abjad.components import Measure
   from abjad.tools import componenttools
   from abjad.tools.marktools.TimeSignatureMark import TimeSignatureMark

   result = [ ]
   if not isinstance(leaf, _Leaf):
      return result
   marks = set([ ])
   for component in componenttools.get_improper_parentage_of_component(leaf):
      #print component.__class__.__name__
      for mark in component.marks:
         #print mark
         if mark._format_slot == slot:
            if mark.start_component is not None:
               if mark.start_component.offset.start == leaf.offset.start:
                  marks.add(mark)
   #print marks
   for mark in marks:
      #print mark, mark.format
      addenda = [ ]
      mark_format = mark.format
      if isinstance(mark_format, (tuple, list)):
         #result.extend(mark_format)
         addenda.extend(mark_format)
      else:
         #result.append(mark_format)
         addenda.append(mark_format)
      ## cosmetic mark is a hack to allow marks to format even without effective context;
      ## currently used only in metric grid formatting
      if mark.effective_context is not None or \
         getattr(mark, '_is_cosmetic_mark', False) or \
         (isinstance(mark, TimeSignatureMark) and
         isinstance(mark.start_component, Measure)):
         result.extend(addenda)         
      else:
         addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
         result.extend(addenda)
   #print result
   #print ''
   result.sort( )
   return result   
