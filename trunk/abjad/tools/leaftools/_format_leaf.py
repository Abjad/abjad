from abjad.tools.formattools._get_articulation_format_contributions import \
   _get_articulation_format_contributions
from abjad.tools.formattools._get_comment_format_contributions_for_slot import \
   _get_comment_format_contributions_for_slot
from abjad.tools.formattools._get_context_mark_format_contributions_for_slot import \
   _get_context_mark_format_contributions_for_slot
from abjad.tools.formattools._get_context_setting_format_contributions import \
   _get_context_setting_format_contributions
from abjad.tools.formattools._get_grob_override_format_contributions import \
   _get_grob_override_format_contributions
from abjad.tools.formattools._get_lilypond_command_mark_format_contributions_for_slot import \
   _get_lilypond_command_mark_format_contributions_for_slot
from abjad.tools.formattools._get_markup_format_contributions import \
   _get_markup_format_contributions
from abjad.tools.formattools._get_spanner_format_contributions_for_leaf_slot import \
   _get_spanner_format_contributions_for_leaf_slot


def _format_leaf(leaf):
   result = [ ]
   result.extend(_get_slot_1(leaf))
   #result.extend(_get_slot_2(leaf))
   result.extend(_get_slot_3(leaf))
   result.extend(_get_slot_4(leaf))
   result.extend(_get_slot_5(leaf))
   #result.extend(_get_slot_6(leaf))
   result.extend(_get_slot_7(leaf))
   contributions = [ ]
   for contributor, contribution in result:
      contributions.extend(contribution)
   return '\n'.join(contributions)
   

def _agrace_body(leaf):
   result = [ ]
   if hasattr(leaf, '_after_grace'):
      after_grace = leaf.after_grace
      if len(after_grace):
         result.append(after_grace.format)
   return result

def _agrace_opening(leaf):
   result = [ ]
   if hasattr(leaf, '_after_grace'):
      if len(leaf.after_grace):
         result.append(r'\afterGrace')
   return result

def _grace_body(leaf):
   result = [ ]
   if hasattr(leaf, '_grace'):
      grace = leaf.grace
      if len(grace):
         result.append(grace.format)
   return result

def _leaf_body(leaf):
   result = [ ]
   client = leaf
   spanners = client.spanners
   result.extend(_nucleus(leaf))
   result.extend(_tremolo_subdivision_contribution(leaf))
   result.extend(_get_articulation_format_contributions(leaf))
   result.extend(_get_lilypond_command_mark_format_contributions_for_slot(leaf, 'right'))
   ## remove next line ##
   result.extend(_get_context_mark_format_contributions_for_slot(leaf, 'right'))
   result.extend(_get_markup_format_contributions(client))
   result.extend(_get_spanner_format_contributions_for_leaf_slot(client, 'right'))
   #result.extend(_number_contribution(leaf))
   result.extend(_get_comment_format_contributions_for_slot(client, 'right'))
   return [' '.join(result)]

def _nucleus(leaf):
   from abjad.components import Chord
   if not isinstance(leaf, Chord):
      return leaf._body
   result =  [ ]
   chord = leaf
   note_heads = chord.note_heads
   if any(['\n' in x.format for x in note_heads]):
      #print 'overrides!'
      for note_head in note_heads:
         format = note_head.format
         format_list = format.split('\n')
         format_list = ['\t' + x for x in format_list]
         result.extend(format_list)
      result.insert(0, '<')
      result.append('>')
      result = '\n'.join(result)
      result += str(chord.duration)
   else:
      #print 'no overrides'
      result.extend([x.format for x in note_heads])
      result = '<%s>%s' % (
         ' '.join(result), chord.duration)
   ## single string, but wrapped in list bc contribution
   return [result]

#def _number_contribution(leaf):
#   result = [ ]
#   leaf = leaf
#      contribution = leaf.number._leaf_contribution
#      if contribution == 'markup':
#         result.append(r'^ \markup { %s }' % leaf.number)
#      elif contribution == 'comment':
#         result.append(r'%% leaf %s' % leaf.number)
#   return result

def _tremolo_subdivision_contribution(leaf):
   result = [ ]
   subdivision = getattr(leaf, 'tremolo_subdivision', None)
   if subdivision:
      result.append(':%s' % subdivision) 
   return result

def _get_slot_1(leaf):
   result = [ ]
   result.append([('grace body', ''), _grace_body(leaf)])
   result.append([('comments', ''), 
      _get_comment_format_contributions_for_slot(leaf, 'before')])
   result.append([('lilypond command marks', ''), 
      _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'before')])
   ## remove next two lines ##
   result.append([('context marks', ''),
      _get_context_mark_format_contributions_for_slot(leaf, 'before')])
   result.append([('grob overrides', ''),
      _get_grob_override_format_contributions(leaf)])
   result.append([('context settings', ''),
      _get_context_setting_format_contributions(leaf)])
   result.append([('spanners', ''),
      _get_spanner_format_contributions_for_leaf_slot(leaf, 'before')])
   return result

def _get_slot_3(leaf):
   result = [ ]
   result.append([('comments', ''), 
      _get_comment_format_contributions_for_slot(leaf, 'opening')])
   result.append([('lilypond command marks', ''), 
      _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'opening')])
   ## remove next two lines ##
   result.append([('context marks', ''),
      _get_context_mark_format_contributions_for_slot(leaf, 'opening')])
   result.append([('agrace opening', ''), _agrace_opening(leaf)])
   return result

def _get_slot_4(leaf):
   result = [ ]
   result.append([('leaf body', ''),
      _leaf_body(leaf)]),
   return result

def _get_slot_5(leaf):
   result = [ ]
   result.append([('agrace body', ''), _agrace_body(leaf)])
   result.append([('lilypond command marks', ''), 
      _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'closing')])
   ## remove next two lines ##
   result.append([('context marks', ''),
      _get_context_mark_format_contributions_for_slot(leaf, 'closing')])
   result.append([('comments', ''), 
      _get_comment_format_contributions_for_slot(leaf, 'closing')])
   return result

def _get_slot_7(leaf):
   result = [ ]
   result.append([('spanners', ''), 
      _get_spanner_format_contributions_for_leaf_slot(leaf, 'after')])
   ## remove next two lines ##
   result.append([('context marks', ''),
      _get_context_mark_format_contributions_for_slot(leaf, 'after')])
   result.append([('lilypond command marks', ''), 
      _get_lilypond_command_mark_format_contributions_for_slot(leaf, 'after')])
   result.append([('comments', ''), 
      _get_comment_format_contributions_for_slot(leaf, 'after')])
   return result
