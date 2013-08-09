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
        return self[0]._get_effective_context_mark(
            context_mark_classes=context_mark_classes,
            )

    def get_effective_staff(self):
        r'''Gets effective staff of component.

        Returns staff or none.
        '''
        return self[0]._get_effective_staff()

    def get_mark(
        self,
        mark_classes=None,
        ):
        r'''Gets exactly one mark of `mark_classes` attached to component.

        Raises exception when no mark of `mark_classes` is attached
        to component.

        Returns mark.
        '''
        return self[0]._get_mark(
            mark_classes=mark_classes,
            )

    def get_marks(
        self,
        mark_classes=None,
        ):
        r'''Get all marks of `mark_classes` attached to component.

        Return tuple.
        '''
        return self[0]._get_marks(
            mark_classes=mark_classes,
            )

    def get_markup(
        self,
        direction=None,
        ):
        r'''Gets all markup attached to component.

        Returns tuple.
        '''
        return self[0]._get_markup(
            direction=direction,
            )

    def get_spanners(self):
        r'''Gets spanners attached to component.

        Returns set.
        '''
        return self[0]._get_spanners()
