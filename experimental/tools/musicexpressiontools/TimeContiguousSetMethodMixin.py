# -*- encoding: utf-8 -*-
import copy
from abjad.tools import systemtools
from experimental.tools.musicexpressiontools.SetMethodMixin \
    import SetMethodMixin


class TimeContiguousSetMethodMixin(SetMethodMixin):
    r'''Set method mixin.

    Segment definition for examples:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that implement the set method interface.
    '''

    ### PRIVATE METHODS ###

    def _store_multiple_context_set_expression(
        self,
        attribute,
        source_expression,
        contexts=None,
        persist=True,
        truncate=None,
        ):
        from experimental.tools import musicexpressiontools
        source_expression = self._expr_to_expression(source_expression)
        assert self.score_specification is not None
        scope_names = self.score_specification._context_token_to_context_names(contexts)
        multiple_context_set_expression = musicexpressiontools.MultipleContextSetExpression(
            attribute=attribute,
            source_expression=source_expression,
            target_timespan=self._expression_abbreviation,
            scope_names=scope_names,
            persist=persist,
            truncate=truncate,
            )
        multiple_context_set_expression._score_specification = \
            self.score_specification
        multiple_context_set_expression._lexical_rank = \
            self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        self.score_specification.multiple_context_set_expressions.append(
            multiple_context_set_expression)
        return multiple_context_set_expression

    ### PUBLIC METHODS ###

    def set_divisions(
        self,
        source_expression,
        contexts=None,
        persist=True,
        truncate=None,
        ):
        r'''Set divisions to `source_expression` for target timespan over 
        all `contexts`:

        Example. Set divisions to ``3/16`` for red segment timespan over 
        contexts ``'Voice 1'`` and ``'Voice 3'``:

        ::

            >>> set_expression = red_segment.set_divisions(
            ...     [(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> print format(set_expression)
            musicexpressiontools.MultipleContextSetExpression(
                attribute='divisions',
                source_expression=musicexpressiontools.IterablePayloadExpression(
                    payload=(
                        (3, 16),
                        ),
                    ),
                target_timespan='red',
                scope_names=['Voice 1', 'Voice 3'],
                persist=True,
                )

        Returns multiple-context set expression.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_set_expression(
            attribute,
            source_expression,
            contexts=contexts,
            truncate=truncate,
            persist=persist,
            )

    def set_rhythm(
        self,
        source_expression,
        contexts=None,
        persist=True,
        ):
        r'''Set rhythm to `source_expression` for target timespan 
        over all `contexts`.

        Example. Set rhythm to sixteenths for red segment target timespan
        over all contexts:

        ::

            >>> set_expression = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> print format(set_expression)
            musicexpressiontools.MultipleContextSetExpression(
                attribute='rhythm',
                source_expression=musicexpressiontools.RhythmMakerExpression(
                    payload=rhythmmakertools.TaleaRhythmMaker(
                        talea=[1],
                        talea_denominator=16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False,
                        ),
                    ),
                target_timespan='red',
                persist=True,
                )

        Returns multiple-context set expression.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_set_expression(
            attribute,
            source_expression,
            contexts=contexts,
            persist=persist,
            )

    def set_time_signatures(
        self,
        source_expression,
        contexts=None,
        persist=True,
        ):
        r'''Set time signatures to `source_expression` for target timespan 
        over all `contexts`.

        Example. Set time signatures to ``3/8``, ``4/8`` for red 
        segment timespan over all contexts:

        ::

            >>> set_expression = red_segment.set_time_signatures(
            ...     [(3, 8), (4, 8)])

        ::

            >>> print format(set_expression)
            musicexpressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                source_expression=musicexpressiontools.IterablePayloadExpression(
                    payload=(
                        (3, 8),
                        (4, 8),
                        ),
                    ),
                target_timespan='red',
                persist=True,
                )

        Returns multiple-context set expression.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_set_expression(
            attribute,
            source_expression,
            contexts=contexts,
            persist=persist,
            )
