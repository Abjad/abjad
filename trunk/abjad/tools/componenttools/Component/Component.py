import abc
import copy
import fractions
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import lilypondproxytools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class Component(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_duration', '_is_forbidden_to_update', '_marks_are_current',
        '_marks_for_which_component_functions_as_effective_context',
        '_marks_for_which_component_functions_as_start_component', 
        '_offset', '_offset_values_in_seconds_are_current', '_override', '_parent', 
        '_prolated_offset_values_are_current', '_set', '_spanners', 
        '_start_offset', '_start_offset_in_seconds', '_stop_offset', '_stop_offset_in_seconds', 
        'lilypond_file', )

    ### INITIALIZER ###

    def __init__(self):
        self._is_forbidden_to_update = False
        self._marks_are_current = False
        self._marks_for_which_component_functions_as_effective_context = list()
        self._marks_for_which_component_functions_as_start_component = list()
        self._offset_values_in_seconds_are_current = False
        self._parent = None
        self._prolated_offset_values_are_current = False
        self._spanners = set([])
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        from abjad.tools import marktools
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in marktools.get_marks_attached_to_component(self):
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        return new

    def __getnewargs__(self):
        return ()

    def __mul__(self, n):
        from abjad.tools import componenttools
        return componenttools.copy_components_and_remove_spanners([self], n)

    def __rmul__(self, n):
        return self * n

    ### PRIVATE PROPERTIES ###

    @property
    def _id_string(self):
        lhs = self._class_name
        rhs = getattr(self, 'name', None) or id(self)
        return '{}-{!r}'.format(lhs, rhs)

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    @property
    def _prolations(self):
        result = []
        parent = self.parent
        while parent is not None:
            result.append(getattr(parent, 'multiplier', fractions.Fraction(1)))
            parent = parent.parent
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    @property
    def override(self):
        '''Read-only reference to LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def parent(self):
        return self._parent

    @property
    def prolated_duration(self):
        return self.prolation * self.preprolated_duration

    @property
    def prolation(self):
        products = mathtools.cumulative_products([fractions.Fraction(1)] + self._prolations)
        return products[-1]

    @property
    def set(self):
        '''Read-only reference LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = lilypondproxytools.LilyPondContextSettingComponentPlugIn()
        return self._set

    @property
    def spanners(self):
        '''Read-only reference to unordered set of spanners attached to component.
        '''
        return set(self._spanners)

    @property
    def start_offset(self):
        '''Read-only start offset of component.
        '''
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._start_offset

    @property
    def start_offset_in_seconds(self):
        '''Read-only start offset of comonent in seconds.
        '''
        self._update_marks_of_entire_score_tree_if_necessary()
        if self._start_offset_in_seconds is None:
            raise MissingTempoError
        return self._start_offset_in_seconds

    @property
    def stop_offset(self):
        '''Read-only stop offset of component.
        '''
        return self.start_offset + self.prolated_duration

    @property
    def stop_offset_in_seconds(self):
        '''Read-only stop offset of component in seconds.
        '''
        return self.start_offset_in_seconds + self.duration_in_seconds

    ### PRIVATE METHODS ###

    def _cut(self):
        '''Component loses pointer to parent and parent loses pointer to component.
        Not composer-safe.
        '''
        if self.parent is not None:
            index = self.parent.index(self)
            self.parent._music.pop(index)
        self._ignore()

    def _ignore(self):
        '''Component loses pointer to parent but parent preserves pointer to component.
        Not composer-safe.
        '''
        self._mark_entire_score_tree_for_later_update('prolated')
        self._parent = None

    def _switch(self, new_parent):
        '''Component loses pointer to parent and parent loses pointer to component.
        Then assign component to new parent.
        '''
        from abjad.tools import componenttools

        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.iteritems():
                name_dictionary[name] = copy.copy(children)
        if hasattr(self, 'name') and self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = []
            name_dictionary[self.name].append(self)

        if self._parent is not None and name_dictionary:
            parentage = componenttools.get_proper_parentage_of_component(self)
            for parent in parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

        self._cut()
        self._parent = new_parent

        if new_parent is not None and name_dictionary:
            parentage = componenttools.get_proper_parentage_of_component(self)
            for parent in parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

        self._mark_entire_score_tree_for_later_update('prolated')

    def _format_component(self, pieces=False):
        result = []
        format_contributions = formattools.get_all_format_contributions(self)
        result.extend(self._format_before_slot(format_contributions))
        result.extend(self._format_open_brackets_slot(format_contributions))
        result.extend(self._format_opening_slot(format_contributions))
        result.extend(self._format_contents_slot(format_contributions))
        result.extend(self._format_closing_slot(format_contributions))
        result.extend(self._format_close_brackets_slot(format_contributions))
        result.extend(self._format_after_slot(format_contributions))
        contributions = []
        for contributor, contribution in result:
            contributions.extend(contribution)
        if pieces:
            return contributions
        else:
            return '\n'.join(contributions)

    def _format_after_slot(self, format_contributions):
        pass

    def _format_before_slot(self, format_contributions):
        pass

    def _format_close_brackets_slot(self, format_contributions):
        pass

    def _format_closing_slot(self, format_contributions):
        pass

    def _format_contents_slot(self, format_contributions):
        pass

    def _format_open_brackets_slot(self, format_contributions):
        pass

    def _format_opening_slot(self, format_contributions):
        pass

    def _get_format_contributions_for_slot(self, n, format_contributions=None):
        if format_contributions is None:
            format_contributions = formattools.get_all_format_contributions(self)
        result = []
        slots = ('before', 'open_brackets', 'opening',
            'contents', 'closing', 'close_brackets', 'after')
        if isinstance(n, str):
            n = n.replace(' ', '_')
        elif isinstance(n, int):
            n = slots[n-1]
        attr = getattr(self, '_format_{}_slot'.format(n))
        for source, contributions in attr(format_contributions):
            result.extend(contributions)
        return result

    def _initialize_keyword_values(self, **kwargs):
        for key, value in kwargs.iteritems():
            self._set_keyword_value(key, value)

    def _set_keyword_value(self, key, value):
        attribute_chain = key.split('__')
        plug_in_name = attribute_chain[0]
        names = attribute_chain[1:]
        if plug_in_name == 'duration':
            attribute_name = names[0]
            command = 'self.%s.%s = %r' % (plug_in_name, attribute_name, value)
            print command
            if 'multiplier' not in command:
                exec(command)
        elif plug_in_name == 'override':
            if len(names) == 2:
                grob_name, attribute_name = names
                exec('self.override.%s.%s = %r' % (grob_name, attribute_name, value))
            elif len(names) == 3:
                context_name, grob_name, attribute_name = names
                exec('self.override.%s.%s.%s = %r' % (
                    context_name, grob_name, attribute_name, value))
            else:
                raise ValueError
        elif plug_in_name == 'set':
            if len(names) == 1:
                setting_name = names[0]
                exec('self.set.%s = %r' % (setting_name, value))
            elif len(names) == 2:
                context_name, setting_name = names
                exec('self.set.%s.%s = %r' % (context_name, setting_name, value))
            else:
                raise ValueError
        else:
            raise ValueError('\n\t: Unknown keyword argument plug-in name: "%s".' % plug_in_name)

    ### MANGLED METHODS ###

    def _update_leaf_indices_and_measure_numbers_in_score_tree(self):
        '''Called only when updating prolated offset of score components.
        No separate state flags for leaf indices or measure numbers.
        '''
        from abjad.tools import componenttools
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import measuretools
        from abjad.tools.contexttools.Context import Context
        score_root = componenttools.component_to_score_root(self)
        if isinstance(score_root, Context):
            for context in iterationtools.iterate_contexts_in_expr(score_root):
                for leaf_index, leaf in enumerate(iterationtools.iterate_leaves_in_expr(context)):
                    leaf._leaf_index = leaf_index
                for measure_index, measure in enumerate(
                    iterationtools.iterate_measures_in_expr(context)):
                    measure_number = measure_index + 1
                    measure._measure_number = measure_number
        else:
            for leaf_index, leaf in enumerate(iterationtools.iterate_leaves_in_expr(score_root)):
                leaf._leaf_index = leaf_index
            for measure_index, measure in enumerate(
                iterationtools.iterate_measures_in_expr(score_root)):
                measure_number = measure_index + 1
                measure._measure_number = measure_number

    def _update_marks_of_entire_score_tree(self):
        '''Updating marks does not cause prolated offset values to update.
        On the other hand, getting effective mark causes prolated offset values
        to update when at least one mark of appropriate type attaches to score.
        '''
        components = self._iterate_score_components_depth_first()
        for component in components:
            for mark in component._marks_for_which_component_functions_as_start_component:
                if hasattr(mark, '_update_effective_context'):
                    mark._update_effective_context()
            component._marks_are_current = True

    def _update_offset_values_in_seconds_of_entire_score_tree(self):
        from abjad.tools import offsettools
        components = self._iterate_score_components_depth_first()
        for component in components:
            offsettools.update_offset_values_of_component_in_seconds(component)
            component._offset_values_in_seconds_are_current = True

    def _update_prolated_offset_values_of_entire_score_tree(self):
        '''Updating prolated offset values does NOT update marks.
        Updating prolated offset values does NOT update offset values in seconds.
        '''
        from abjad.tools import offsettools
        components = self._iterate_score_components_depth_first()
        for component in components:
            offsettools.update_offset_values_of_component(component)
            component._prolated_offset_values_are_current = True

    ### PRIVATE UPDATE METHODS ###

    def _allow_component_update(self):
        self._is_forbidden_to_update = False

    def _forbid_component_update(self):
        self._is_forbidden_to_update = True

    def _get_score_tree_state_flags(self):
        from abjad.tools import componenttools
        prolated_offset_values_are_current = True
        marks_are_current = True
        offset_values_in_seconds_are_current = True
        for component in componenttools.get_improper_parentage_of_component(self):
            if prolated_offset_values_are_current:
                if not component._prolated_offset_values_are_current:
                    prolated_offset_values_are_current = False
            if marks_are_current:
                if not component._marks_are_current:
                    marks_are_current = False
            if offset_values_in_seconds_are_current:
                if not component._offset_values_in_seconds_are_current:
                    offset_values_in_seconds_are_current = False
        return (prolated_offset_values_are_current, marks_are_current,
            offset_values_in_seconds_are_current)

    def _iterate_score_components_depth_first(self):
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        score_root = componenttools.component_to_score_root(self)
        kwargs = {'capped': True, 'unique': True, 'forbid': None, 'direction': 'left'}
        components = iterationtools.iterate_components_depth_first(score_root, **kwargs)
        return components

    def _mark_entire_score_tree_for_later_update(self, value):
        '''Call immediately AFTER MODIFYING score tree.
        Only dynamic measures mark time signature for udpate.
        '''
        from abjad.tools import componenttools
        assert value in ('prolated', 'marks', 'seconds')
        for component in componenttools.get_improper_parentage_of_component(self):
            if value == 'prolated':
                component._prolated_offset_values_are_current = False
            elif value == 'marks':
                component._marks_are_current = False
            elif value == 'seconds':
                component._offset_values_in_seconds_are_current = False
            else:
                raise ValueError('unknown value: "%s"' % value)
            if hasattr(component, '_time_signature_is_current'):
                component._time_signature_is_current = False

    def _update_marks_of_entire_score_tree_if_necessary(self):
        '''Call immediately BEFORE READING effective mark.
        '''
        if self._is_forbidden_to_update:
            return
        state_flags = self._get_score_tree_state_flags()
        marks_are_current = state_flags[1]
        if not marks_are_current:
            self._update_marks_of_entire_score_tree()
            self._update_offset_values_in_seconds_of_entire_score_tree()

    def _update_prolated_offset_values_of_entire_score_tree_if_necessary(self):
        if self._is_forbidden_to_update:
            return
        state_flags = self._get_score_tree_state_flags()
        prolated_offset_values_are_current = state_flags[0]
        if not prolated_offset_values_are_current:
            self._update_prolated_offset_values_of_entire_score_tree()
            self._update_leaf_indices_and_measure_numbers_in_score_tree()
