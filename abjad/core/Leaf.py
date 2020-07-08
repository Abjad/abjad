import abc
import copy
import typing

from .. import exceptions
from ..bundle import LilyPondFormatBundle
from ..duration import Duration, Multiplier, NonreducedFraction
from ..indicators.MetronomeMark import MetronomeMark
from ..overrides import override, setting
from ..storage import FormatSpecification
from ..tags import Tag
from .Component import Component, attach


class Leaf(Component):
    """
    Leaf baseclass.

    Leaves include notes, rests, chords and skips.
    """

    ### CLASS VARIABLES ##

    _allowable_format_slots = (
        "absolute_before",
        "before",
        "after",
        "absolute_after",
    )

    __slots__ = (
        "_after_grace_container",
        "_before_grace_container",
        "_multiplier",
        "_written_duration",
    )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration, *, multiplier=None, tag: Tag = None) -> None:
        Component.__init__(self, tag=tag)
        self._after_grace_container = None
        self._before_grace_container = None
        self.multiplier = multiplier
        self.written_duration = written_duration

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies leaf.
        """
        new = Component.__copy__(self, *arguments)
        new.multiplier = self.multiplier
        before_grace_container = self._before_grace_container
        if before_grace_container is not None:
            new_grace_container = before_grace_container._copy_with_children()
            attach(new_grace_container, new)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            new_after_grace_container = after_grace_container._copy_with_children()
            attach(new_after_grace_container, new)
        return new

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return (self.written_duration,)

    def __str__(self) -> str:
        """
        Gets string representation of leaf.
        """
        return self._get_compact_representation()

    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, "_overrides", None) is not None:
            self._overrides = copy.copy(override(leaf))
        if getattr(leaf, "_lilypond_setting_name_manager", None) is not None:
            self._lilypond_setting_name_manager = copy.copy(setting(leaf))
        new_wrappers = []
        for wrapper in leaf._wrappers:
            new_wrapper = copy.copy(wrapper)
            new_wrappers.append(new_wrapper)
        for new_wrapper in new_wrappers:
            attach(new_wrapper, self)

    def _format_after_grace_body(self):
        result = []
        container = self._after_grace_container
        if container is not None:
            result.append(format(container))
        return result

    def _format_after_grace_command(self):
        result = []
        if self._after_grace_container is not None:
            result.append(r"\afterGrace")
        return result

    def _format_after_slot(self, bundle):
        result = []
        result.append(("stem_tremolos", bundle.after.stem_tremolos))
        result.append(("articulations", bundle.after.articulations))
        result.append(("markup", bundle.after.markup))
        result.append(("spanners", bundle.after.spanners))
        result.append(("spanner_stops", bundle.after.spanner_stops))
        result.append(("spanner_starts", bundle.after.spanner_starts))
        # NOTE: LilyPond demands \startTrillSpan appear after almost all
        #       other format contributions; pitched trills dangerously
        #       suppress markup and the starts of other spanners when
        #       \startTrillSpan appears lexically prior to those commands;
        #       but \startTrillSpan must appear before calls to \set.
        result.append(("trill_spanner_starts", bundle.after.trill_spanner_starts))
        result.append(("commands", bundle.after.commands))
        result.append(("commands", bundle.after.leaks))
        result.append(("after grace body", self._format_after_grace_body()))
        result.append(("comments", bundle.after.comments))
        return result

    def _format_before_slot(self, bundle):
        result = []
        result.append(("grace body", self._format_grace_body()))
        result.append(("comments", bundle.before.comments))
        result.append(("commands", bundle.before.commands))
        result.append(("indicators", bundle.before.indicators))
        result.append(("grob reverts", bundle.grob_reverts))
        result.append(("grob overrides", bundle.grob_overrides))
        result.append(("context settings", bundle.context_settings))
        result.append(("spanners", bundle.before.spanners))
        return result

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("spanners", bundle.closing.spanners))
        result.append(("commands", bundle.closing.commands))
        result.append(("indicators", bundle.closing.indicators))
        result.append(("comments", bundle.closing.comments))
        return result

    def _format_contents_slot(self, bundle):
        result = []
        result.append(("leaf body", self._format_leaf_body(bundle)))
        return result

    def _format_grace_body(self):
        result = []
        container = self._before_grace_container
        if container is not None:
            result.append(format(container))
        return result

    def _format_leaf_body(self, bundle):
        result = self._format_leaf_nucleus()
        return result

    def _format_leaf_nucleus(self):
        strings = self._get_body()
        if self.tag:
            tag = Tag(self.tag)
            strings = Tag.tag(strings, tag=tag)
        return strings

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("indicators", bundle.opening.indicators))
        result.append(("commands", bundle.opening.commands))
        result.append(("spanners", bundle.opening.spanners))
        # IMPORTANT: LilyPond \afterGrace must appear IMMEDIATELY before leaf!
        result.append(("after grace command", self._format_after_grace_command()))
        return result

    def _get_compact_representation(self):
        return f"({self._get_formatted_duration()})"

    def _get_duration_in_seconds(self):
        mark = self._get_effective(MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                self._get_duration()
                / mark.reference_duration
                / mark.units_per_minute
                * 60
            )
            return Duration(result)
        raise exceptions.MissingMetronomeMarkError

    def _get_format_pieces(self):
        return self._get_lilypond_format().split("\n")

    def _get_format_specification(self):
        summary = self._get_compact_representation()
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[summary],
            storage_format_args_values=[format(self, "lilypond")],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
        )

    def _get_formatted_duration(self):
        strings = []
        strings.append(self.written_duration.lilypond_duration_string)
        if self.multiplier is not None:
            strings.append(str(self.multiplier))
        if hasattr(self._parent, "_leaf_multiplier"):
            multiplier = self._parent._leaf_multiplier()
            if multiplier is not None:
                strings.append(str(multiplier))
        result = " * ".join(strings)
        return result

    def _get_multiplied_duration(self):
        if self.written_duration:
            if self.multiplier is not None:
                duration = self.multiplier * self.written_duration
                return Duration(duration)
            return Duration(self.written_duration)

    def _get_preprolated_duration(self):
        return self._get_multiplied_duration()

    def _process_contribution_packet(self, contribution_packet):
        result = ""
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = LilyPondFormatBundle.indent + contributor[0] + ":\n"
                else:
                    contributor = LilyPondFormatBundle.indent + contributor + ":\n"
                result += contributor
                for contribution in contributions:
                    contribution = (
                        (LilyPondFormatBundle.indent * 2) + contribution + "\n"
                    )
                    result += contribution
        return result

    def _scale(self, multiplier):
        self.written_duration *= multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def multiplier(self) -> typing.Union[Multiplier, NonreducedFraction, None]:
        """
        Gets multiplier.
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        if isinstance(argument, (NonreducedFraction, type(None))):
            multiplier = argument
        else:
            multiplier = Multiplier(argument)
        self._multiplier = multiplier

    @property
    def written_duration(self) -> Duration:
        """
        Gets written duration.
        """
        return self._written_duration

    @written_duration.setter
    def written_duration(self, argument):
        duration = Duration(argument)
        if not duration.is_assignable:
            message = f"not assignable duration: {duration!r}."
            raise exceptions.AssignabilityError(message)
        self._written_duration = duration
