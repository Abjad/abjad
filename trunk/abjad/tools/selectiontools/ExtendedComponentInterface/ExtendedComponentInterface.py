# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class ExtendedComponentInterface(Selection):
    r'''Access to extended component methods.
    '''

    ### PUBLIC METHODS ###

    def get_annotation_value(self, name, default=None):
        r'''Gets value of annotation with `name` attached to component.

        Returns `default` when no annotation with `name` is attached
        to component.

        Raises exception when more than one annotation with `name`
        is attached to component.
        '''
        from abjad.tools import marktools
        annotations = self.get_marks(marktools.Annotation)
        if not annotations:
            return default
        with_correct_name = []
        for annotation in annotations:
            if annotation.name == name:
                with_correct_name.append(annotation)
        if not with_correct_name:
            return default
        if 1 < len(with_correct_name):
            raise Exception('more than one annotation.')
        annotation_value = with_correct_name[0].value
        return annotation_value

    def get_effective_context_mark(
        self,
        context_mark_classes=None,
        ):
        r'''Gets effective context mark of `context_mark_class` 
        that governs component.

        Returns context mark or none.
        '''
        from abjad.tools import contexttools
        from abjad.tools import datastructuretools
        from abjad.tools import measuretools
        # do special things for time signature marks
        if context_mark_classes == contexttools.TimeSignatureMark:
            if isinstance(self[0], measuretools.Measure):
                if self[0]._has_mark(contexttools.TimeSignatureMark):
                    return self[0].get_mark(contexttools.TimeSignatureMark)
        # updating marks of entire score tree if necessary
        self[0]._update_marks_of_entire_score_tree_if_necessary()
        # gathering candidate marks
        candidate_marks = datastructuretools.SortedCollection(
            key=lambda x: x.start_component.get_timespan().start_offset)
        for parent in self[0].select_parentage(include_self=True):
            parent_marks = parent._dependent_context_marks
            for mark in parent_marks:
                if isinstance(mark, context_mark_classes):
                    if mark.effective_context is not None:
                        candidate_marks.insert(mark)
                    elif isinstance(mark, contexttools.TimeSignatureMark):
                        if isinstance(
                            mark.start_component, measuretools.Measure):
                            candidate_marks.insert(mark)
        # elect most recent candidate mark
        if candidate_marks:
            try:
                start_offset = self[0].get_timespan().start_offset
                return candidate_marks.find_le(start_offset)
            except ValueError:
                pass

    def get_effective_staff(self):
        r'''Gets effective staff of component.

        Returns staff or none.
        '''
        from abjad.tools import contexttools
        from abjad.tools import stafftools
        staff_change_mark = self.get_effective_context_mark(
            contexttools.StaffChangeMark)
        if staff_change_mark is not None:
            effective_staff = staff_change_mark.staff
        else:
            parentage = self[0].select_parentage()
            effective_staff = parentage.get_first(stafftools.Staff)
        return effective_staff

    def get_mark(
        self,
        mark_classes=None,
        ):
        r'''Gets exactly one mark of `mark_classes` attached to component.

        Raises exception when no mark of `mark_classes` is attached
        to component.

        Returns mark.
        '''
        marks = self.get_marks(mark_classes=mark_classes)
        if not marks:
            raise MissingMarkError
        elif 1 < len(marks):
            raise ExtraMarkError
        else:
            return marks[0]

    def get_marks(
        self,
        mark_classes=None,
        ):
        r'''Get all marks of `mark_classes` attached to component.

        Return tuple.
        '''
        from abjad.tools import marktools
        mark_classes = mark_classes or (marktools.Mark,)
        if not isinstance(mark_classes, tuple):
            mark_classes = (mark_classes,)
        marks = []
        for mark in self[0]._start_marks:
            if isinstance(mark, mark_classes):
                marks.append(mark)
        return tuple(marks)

    def get_markup(
        self,
        direction=None,
        ):
        r'''Gets all markup attached to component.

        Returns tuple.
        '''
        from abjad.tools import markuptools
        markup = self.get_marks(mark_classes=(markuptools.Markup,))
        if direction is Up:
            return tuple(x for x in markup if x.direction is Up)
        elif direction is Down:
            return tuple(x for x in markup if x.direction is Down)
        return markup

    def get_spanners(self):
        r'''Gets spanners attached to component.

        Returns set.
        '''
        return set(self[0]._spanners)
