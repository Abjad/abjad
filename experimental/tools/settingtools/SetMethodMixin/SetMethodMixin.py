import copy
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''Setting-maker mix-in.

    ::
        
        >>> from experimental.tools import *

    Examples below use the score and segment specification defined here::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Equips classes with the composer setting-maker interface.
    '''

    ### PRIVATE METHODS ###

    def _expr_to_request(self, expr):
        from abjad.tools import rhythmmakertools
        from experimental.tools import handlertools
        from experimental.tools import requesttools
        from experimental.tools import settingtools
        from experimental.tools import statalservertools
        from experimental.tools import timeexpressiontools
        # probably precautionary: prune expr of any incoming references
        expr = copy.deepcopy(expr)
        if isinstance(expr, settingtools.PayloadCallbackMixin):
            return expr
        elif isinstance(expr, statalservertools.StatalServer):
            return requesttools.StatalServerRequest(expr)
        elif isinstance(expr, handlertools.Handler):
            return requesttool.HandlerRequest(expr)
        elif isinstance(expr, (tuple, list, str)):
            return requesttools.AbsoluteRequest(expr)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return requesttools.RhythmMakerRequest(expr)
        else:
            raise TypeError('do not know how to change {!r} to request.'.format(expr))

    def _store_multiple_context_setting(self, attribute, source, contexts=None, persist=True, truncate=None):
        from experimental.tools import settingtools
        request = self._expr_to_request(source)
        assert self.score_specification is not None
        context_names = self.score_specification._context_token_to_context_names(contexts)
        multiple_context_setting = settingtools.MultipleContextSetting(
            attribute,
            request,
            self._anchor_abbreviation,
            context_names=context_names,
            persist=persist,
            truncate=truncate
            )
        self.score_specification.multiple_context_settings.append(multiple_context_setting)
        return multiple_context_setting

    ### PUBLIC METHODS ###

    def set_aggregate(self, source, contexts=None, persist=True):
        r'''Set aggregate of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_articulations(self, source, contexts=None, persist=True):
        r'''Set articulations of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_chord_treatment(self, source, contexts=None, persist=True):
        r'''Set chord treatment of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_divisions(self, source, contexts=None, persist=True, truncate=None):
        r'''Set divisions `contexts` to `source`::

            >>> setting = red_segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='divisions',
                request=requesttools.AbsoluteRequest(
                    ((3, 16),)
                    ),
                anchor='red',
                context_names=['Voice 1', 'Voice 3'],
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_setting(attribute, source,
            contexts=contexts, truncate=truncate, persist=persist)

    def set_dynamics(self, source, contexts=None, persist=True):
        r'''Set dynamics of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_marks(self, source, contexts=None, persist=True):
        r'''Set marks of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'marks'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_markup(self, source, contexts=None, persist=True):
        r'''Set markup of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'markup'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_class_application(self, source, contexts=None, persist=True):
        r'''Set pitch-class application of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_class_transform(self, source, contexts=None, persist=True):
        r'''Set pitch-class transform of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_classes(self, source, contexts=None, persist=True):
        r'''Set pitch-classes of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_registration(self, source, contexts=None, persist=True):
        r'''Set registration of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'registration'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_rhythm(self, source, contexts=None, persist=True):
        r'''Set rhythm of `contexts` to `source`.

            >>> setting = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='rhythm',
                request=requesttools.RhythmMakerRequest(
                    rhythmmakertools.TaleaRhythmMaker(
                        [1],
                        16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        )
                    ),
                anchor='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_setting(attribute, source, contexts=contexts, persist=persist)

    def set_tempo(self, source, contexts=None, persist=True):
        r'''Set tempo of `contexts` to `source`.

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_setting(attribute, source, 
            contexts=contexts, persist=persist)

    def set_time_signatures(self, source, contexts=None, persist=True):
        r'''Set time signatures of `contexts` to `source`.

            >>> setting = red_segment.set_time_signatures([(3, 8), (4, 8)])

        ::

            >>> z(setting)
            settingtools.MultipleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    ((3, 8), (4, 8))
                    ),
                anchor='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetting``.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_setting(attribute, source, contexts=contexts, persist=persist)
