import copy
from experimental import helpertools
from experimental.settingtools.Setting import Setting


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

    def __init__(self, 
        attribute, source, selector, context_name=None, fresh=True, persist=True, truncate=None):
        Setting.__init__(self, attribute, source, selector, fresh=fresh, persist=persist, truncate=truncate)
        assert isinstance(context_name, (str, type(None)))
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Single-context setting context name.

        Return string or none.
        '''
        return self._context_name

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

        Set new setting `fresh` to false.

        Set new setting selector to `segment`.

        Return new setting.
        '''
        new_setting = copy.deepcopy(self)
        new_setting._fresh = False
        segment_name = helpertools.expr_to_segment_name(segment)
        new_setting.selector.set_segment_identifier(segment_name)
        return new_setting
