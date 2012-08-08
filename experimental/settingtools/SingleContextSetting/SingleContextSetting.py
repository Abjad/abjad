from experimental import helpertools
from experimental.settingtools.Setting import Setting
import copy


class SingleContextSetting(Setting):
    r'''.. versionadded:: 1.0

    Single-context setting::

        >>> from abjad.tools import *
        >>> from experimental import *

    Set `attribute` to `source` for single-context `selector`::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.append_segment('red')

    ::

        >>> multiple_context_setting = segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> contexts = ['Voice 1', 'Voice 3']
        >>> multiple_context_setting = segment.set_divisions([(3, 16)], contexts=contexts)

    ::

        >>> score = score_specification.interpret()

    ::

        >>> single_context_setting = score_specification.single_context_settings[1]

    ::

        >>> z(single_context_setting)
        settingtools.SingleContextSetting(
            'divisions',
            [(3, 16)],
            selectortools.SingleSegmentSelector(
                identifier='red'
                ),
            context_name='Voice 1',
            persist=True,
            truncate=False,
            fresh=True
            )

    Composers do not create single-context settings.

    Single-context settings are a byprodct of interpretation.

    Multiple-context settings unpack to produce single-context settings.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, source, selector, context_name=None, persist=True, truncate=False, fresh=True):
        Setting.__init__(self, attribute, source, selector, persist=persist, truncate=truncate)
        assert isinstance(context_name, (str, type(None)))
        assert isinstance(fresh, bool)
        self._fresh = fresh
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Single-context setting context name.

        Return string or none.
        '''
        return self._context_name

    @property
    def fresh(self):
        '''True when single-context setting has been newly specified::

            >>> single_context_setting.fresh
            True

        Need to clarify relationship between `persist` and `fresh` keywords.

        Return boolean.
        '''
        return self._fresh

    @property
    def storage_format(self):
        '''Single-context setting storage format::

            >>> z(single_context_setting)
            settingtools.SingleContextSetting(
                'divisions',
                [(3, 16)],
                selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                context_name='Voice 1',
                persist=True,
                truncate=False,
                fresh=True
                )

        Return string.
        '''
        return Setting.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def copy_setting_to_segment(self, segment):
        '''Create new setting. 

        Set new setting to `segment`.

        Set new setting `fresh` to false.

        [Only works when self selector is already a segment selector.]

        Return new setting.
        '''
        #assert self.selector.timespan.encompasses_one_segment_exactly, repr(self)
        new_setting = copy.deepcopy(self)
        new_setting.set_selector_to_segment(segment)
        new_setting._fresh = False
        return new_setting

    def set_selector_to_segment(self, segment):
        '''Set selector to `segment`.

        [Only works when selector is already segment selector.]

        Return none.
        '''
        from experimental import selectortools
        assert isinstance(self.selector, selectortools.SingleSegmentSelector) 
        segment_name = helpertools.expr_to_segment_name(segment)
        segment_selector = selectortools.SingleSegmentSelector(identifier=segment_name)
        self._selector = segment_selector
