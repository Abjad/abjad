from abjad.components.Measure import Measure
from abjad.components.Tuplet import Tuplet
from abjad.tools import contexttools
from abjad.tools.componenttools._get_leaf_keyword_attributes import _get_leaf_keyword_attributes


def _container_to_pitch_and_rhythm_skeleton(container, include_keyword_attributes = False):
   ## late intrapackage import because the functions call each other recursively
   from abjad.tools import componenttools
   from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
   class_name = container.__class__.__name__
   contents = [ ]
   for x in container:
      if include_keyword_attributes:
         skeleton = \
            componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(x)
      else:
         skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(x)
      skeleton = skeleton.split('\n')
      skeleton = ['\t' + line for line in skeleton]
      skeleton = '\n'.join(skeleton)
      contents.append(skeleton)
   contents = ',\n'.join(contents)
   if include_keyword_attributes:
      keyword_attributes = _get_leaf_keyword_attributes(container)
   else:
      keyword_attributes = [ ]
   if keyword_attributes:
      keyword_attributes = ',\n'.join(keyword_attributes)
      keyword_attributes = '\n' + keyword_attributes
   if isinstance(container, Measure):
      meter = repr(contexttools.get_effective_time_signature(container))
      return '%s(%s, [\n%s\n])' % (class_name, meter, contents)
   elif isinstance(container, FixedDurationTuplet):
      duration = repr(container.duration.target)
      if keyword_attributes:
         return '%s(%s, [\n%s\n], %s)' % (class_name, duration, contents, keyword_attributes)
      else:
         return '%s(%s, [\n%s\n])' % (class_name, duration, contents)
   elif isinstance(container, Tuplet):
      multiplier = repr(container.duration.multiplier)
      if keyword_attributes:
         return '%s(%s, [\n%s\n], %s)' % (class_name, multiplier, contents, keyword_attributes)
      else:
         return '%s(%s, [\n%s\n])' % (class_name, multiplier, contents)
   else:
      if keyword_attributes:
         return '%s([\n%s\n], %s)' % (class_name, contents, keyword_attributes)
      else:
         return '%s([\n%s\n])' % (class_name, contents)
