def get_effective_context_mark(component, klass):
    r'''.. versionadded:: 2.0

    Get effective context mark of `klass` from `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.TimeSignatureMark((4, 8))(staff)
        TimeSignatureMark((4, 8))(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_effective_context_mark(staff[0], contexttools.TimeSignatureMark)
        TimeSignatureMark((4, 8))(Staff{4})


    Return context mark or none.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark
    from abjad.tools.measuretools.Measure import Measure

    if klass == TimeSignatureMark:
        if isinstance(component, Measure):
            if not getattr(component, '_time_signature_is_current', True):
                component._update_time_signature()
            if contexttools.is_component_with_time_signature_mark_attached(component):
                return contexttools.get_time_signature_mark_attached_to_component(component)

    #print 'getting effective context mark mark ...'
    # following line was tested to be completely unnecessary; remove after statal bug fix:
    #component._update_prolated_offset_values_of_entire_score_tree_if_necessary()
    component._update_marks_of_entire_score_tree_if_necessary()

    #print 'gathering candidate marks ...'
    candidate_marks = set([])
    for parent in componenttools.get_improper_parentage_of_component(component):
        parent_marks = parent.marks
        #print 'parent marks %s ...' % str(parent_marks)
        for mark in parent_marks:
            #print 'now checking %s ...' % mark
            if isinstance(mark, klass):
                #print 'mark.effective_context is %s ...' % mark.effective_context
                if mark.effective_context is not None:
                    candidate_marks.add(mark)
                elif isinstance(mark, TimeSignatureMark):
                    if isinstance(mark.start_component, Measure):
                        candidate_marks.add(mark)
    #print 'unsorted canddiate marks %s ...' % candidate_marks
    candidate_marks = sorted(candidate_marks,
        cmp = lambda m, n: cmp(m.start_component._offset.start, n.start_component._offset.start))
    #print candidate_marks
    #for x in candidate_marks:
    #    print x, x.start_component._offset.start
    first_winner = None
    for candidate_mark in reversed(candidate_marks):
        if candidate_mark.start_component._offset.start <= component._offset.start:
            if first_winner is None:
                first_winner = candidate_mark
            elif candidate_mark.start_component._offset.start == \
                first_winner.start_component._offset.start:
                raise ExtraMarkError('%s and %s start at the same time.' % (
                    first_winner, candidate_mark))
            else:
                break
    #print 'first winner is ', first_winner, '\n'
    return first_winner
