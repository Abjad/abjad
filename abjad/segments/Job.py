import typing

from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag
from abjad.system.Tags import Tags
from abjad.top.activate import activate
from abjad.top.deactivate import deactivate
from abjad.utilities.String import String

from .Path import Path

abjad_tags = Tags()
callable_type = typing.Union[str, typing.Callable, None]
activation_type = typing.Tuple[callable_type, str]


class Job(object):
    """
    Job.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_activate",
        "_deactivate",
        "_deactivate_first",
        "_message_zero",
        "_path",
        "_prepend_empty_chord",
        "_skip_file_name",
        "_title",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate: activation_type = None,
        deactivate: activation_type = None,
        deactivate_first: bool = None,
        message_zero: bool = None,
        path: Path = None,
        prepend_empty_chord: bool = None,
        skip_file_name: str = None,
        title: str = None,
    ) -> None:
        self._activate = activate
        self._deactivate = deactivate
        self._deactivate_first = deactivate_first
        self._message_zero = message_zero
        self._path = path
        self._prepend_empty_chord = prepend_empty_chord
        self._skip_file_name = skip_file_name
        self._title = title

    ### SPECIAL METHODS ###

    def __call__(self) -> typing.List[String]:
        """
        Calls job on job ``path``.
        """
        messages = []
        if self.title is not None:
            messages.append(String(self.title).capitalize_start())
        total_count = 0
        if isinstance(self.path, str):
            text = self.path
        if self.deactivate_first is True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, Path):
                        result = self.path.deactivate(
                            match,
                            indent=1,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        result = deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
                        assert result is not None
                        text, count, skipped = result
        if self.activate is not None:
            assert isinstance(self.activate, tuple)
            match, name = self.activate
            if match is not None:
                if isinstance(self.path, Path):
                    result = self.path.activate(
                        match,
                        indent=1,
                        message_zero=True,
                        name=name,
                        skip_file_name=self.skip_file_name,
                    )
                    assert result is not None
                    count, skipped, messages_ = result
                    messages.extend(messages_)
                    total_count += count
                else:
                    assert isinstance(self.path, str)
                    text, count, skipped = activate(
                        text, match, skip_file_name=self.skip_file_name, skipped=True,
                    )
        if self.deactivate_first is not True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, Path):
                        result = self.path.deactivate(
                            match,
                            indent=1,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        text, count, skipped = deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
        if total_count == 0 and not self.message_zero:
            messages = []
        if isinstance(self.path, Path):
            return messages
        else:
            assert isinstance(self.path, str)
            return text

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self):
        """
        Gets activate match / message pair.
        """
        return self._activate

    @property
    def deactivate(self):
        """
        Gets deactivate match / message pair.
        """
        return self._deactivate

    @property
    def deactivate_first(self) -> typing.Optional[bool]:
        """
        Is true when deactivate runs first.
        """
        return self._deactivate_first

    @property
    def message_zero(self) -> typing.Optional[bool]:
        """
        Is true when job returns messages even when no matches are found.
        """
        return self._message_zero

    @property
    def path(self) -> typing.Optional[Path]:
        """
        Gets path.
        """
        return self._path

    @property
    def prepend_empty_chord(self) -> typing.Optional[bool]:
        """
        Is true when deactivate prepends LilyPond empty chord ``<>`` command.
        """
        return self._prepend_empty_chord

    @property
    def skip_file_name(self) -> typing.Optional[str]:
        """
        Gets skip file name.
        """
        return self._skip_file_name

    @property
    def title(self) -> typing.Optional[str]:
        """
        Gets title.
        """
        return self._title

    ### PUBLIC METHODS ###

    @staticmethod
    def color_clefs(path, undo=False) -> "Job":
        """
        Colors clefs.
        """
        name = "clef color"

        def match(tags):
            tags_ = abjad_tags.clef_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring clefs ...",
            )
        else:
            return Job(activate=(match, name), path=path, title="coloring clefs ...")

    @staticmethod
    def color_dynamics(path, undo=False) -> "Job":
        """
        Colors dynamics.
        """
        name = "dynamic color"

        def match(tags):
            tags_ = abjad_tags.dynamic_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring dynamics ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring dynamics ...",
            )

    @staticmethod
    def color_instruments(path, undo=False) -> "Job":
        """
        Colors instruments.
        """
        name = "instrument color"

        def match(tags):
            tags_ = abjad_tags.instrument_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring instruments ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring instruments ...",
            )

    @staticmethod
    def color_margin_markup(path, undo=False) -> "Job":
        """
        Colors margin markup.
        """
        name = "margin markup color"

        def match(tags):
            tags_ = abjad_tags.margin_markup_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title="uncoloring margin markup ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring margin markup ...",
            )

    @staticmethod
    def color_metronome_marks(path, undo=False) -> "Job":
        """
        Colors metronome marks.
        """

        def activate(tags):
            tags_ = abjad_tags.metronome_mark_color_expression_tags(path)
            return bool(set(tags) & set(tags_))

        def deactivate(tags):
            tags_ = abjad_tags.metronome_mark_color_suppression_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(deactivate, "metronome mark color suppression"),
                deactivate=(activate, "metronome mark color expression"),
                path=path,
                title="uncoloring metronome marks ...",
            )
        else:
            return Job(
                activate=(activate, "metronome mark color expression"),
                deactivate=(deactivate, "metronome mark color suppression"),
                path=path,
                title="coloring metronome marks ...",
            )

    @staticmethod
    def color_persistent_indicators(path, undo=False) -> "Job":
        """
        Color persistent indicators.
        """
        name = "persistent indicator"
        activate_name = "persistent indicator color expression"

        def activate(tags):
            tags_ = abjad_tags.persistent_indicator_color_expression_tags(path)
            return bool(set(tags) & set(tags_))

        deactivate_name = "persistent indicator color suppression"

        def deactivate(tags):
            tags_ = abjad_tags.persistent_indicator_color_suppression_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(deactivate, deactivate_name),
                deactivate=(activate, activate_name),
                path=path,
                title=f"uncoloring {name}s ...",
            )
        else:
            return Job(
                activate=(activate, activate_name),
                deactivate=(deactivate, deactivate_name),
                path=path,
                title=f"coloring {name}s ...",
            )

    @staticmethod
    def color_staff_lines(path, undo=False) -> "Job":
        """
        Colors staff lines.
        """
        name = "staff lines color"

        def match(tags):
            tags_ = abjad_tags.staff_lines_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring staff lines ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring staff lines ...",
            )

    @staticmethod
    def color_stage_number_markup(path, undo=False) -> "Job":
        """
        Colors stage number markup.
        """
        name = "stage number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.STAGE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def color_time_signatures(path, undo=False) -> "Job":
        """
        Colors time signatures.
        """
        name = "time signature color"

        def match(tags):
            tags_ = abjad_tags.time_signature_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title="uncoloring time signatures ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring time signatures ...",
            )

    @staticmethod
    def handle_edition_tags(path) -> "Job":
        """
        Handles edition tags.

        The logic here is important:

            * deactivations run first:

                -TAG (where TAG is either my directory or my buildtype)

                +TAG (where TAG is neither my directory nor my buildtype)

            * activations run afterwards:

                TAG_SET such that there exists at least one build-forbid
                    -TAG (equal to neither my directory nor my buildtype) in
                    TAG_SET and such that there exists no -TAG (equal to either
                    my directory or my buildtype) in TAG_SET

                +TAG (where TAG is either my directory or my buildtype)

            Notionally: first we deactivate anything that is tagged EITHER
            specifically against me OR specifically for another build; then we
            activate anything that is deactivated for editions other than me;
            then we activate anything is tagged specifically for me.

        ..  todo: Tests.

        """
        if path.parent.is_segment():
            my_name = "SEGMENT"
        elif path.is_score_build() or path.parent.is_score_build():
            my_name = "SCORE"
        elif path.is_parts() or path.is_part():
            my_name = "PARTS"
        else:
            raise Exception(path)
        this_edition = Tag(f"+{String(my_name).to_shout_case()}")
        not_this_edition = Tag(f"-{String(my_name).to_shout_case()}")
        if path.is_dir():
            directory_name = path.name
        else:
            directory_name = path.parent.name
        this_directory = Tag(f"+{String(directory_name).to_shout_case()}")
        not_this_directory = Tag(f"-{String(directory_name).to_shout_case()}")

        def deactivate(tags) -> bool:
            if not_this_edition in tags:
                return True
            if not_this_directory in tags:
                return True
            for tag in tags:
                if str(tag).startswith("+"):
                    return True
            return False

        def activate(tags) -> bool:
            for tag in tags:
                if tag in [not_this_edition, not_this_directory]:
                    return False
            for tag in tags:
                if str(tag).startswith("-"):
                    return True
            return bool(set(tags) & set([this_edition, this_directory]))

        return Job(
            activate=(activate, "this-edition"),
            deactivate=(deactivate, "other-edition"),
            deactivate_first=True,
            path=path,
            title="handling edition tags ...",
        )

    @staticmethod
    def handle_fermata_bar_lines(path) -> "Job":
        """
        Handles fermata bar lines.
        """
        if path.is__segments():
            path = path.parent

        def activate(tags):
            return bool(set(tags) & set([abjad_tags.FERMATA_MEASURE]))

        deactivate: typing.Optional[callable_type]
        # then deactivate non-EOL tags:
        bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
        if bol_measure_numbers:
            eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
            final_measure_number = path.get_metadatum("final_measure_number")
            if final_measure_number is not None:
                eol_measure_numbers.append(final_measure_number)
            eol_measure_numbers = [Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

            def deactivate(tags):
                if abjad_tags.FERMATA_MEASURE in tags:
                    if not bool(set(tags) & set(eol_measure_numbers)):
                        return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "bar line adjustment"),
            deactivate=(deactivate, "EOL fermata bar line"),
            path=path,
            title="handling fermata bar lines ...",
        )

    @staticmethod
    def handle_mol_tags(path) -> "Job":
        """
        Handles MOL (middle-of-line) tags.
        """
        if path.is__segments():
            path = path.parent

        # activate all middle-of-line tags
        def activate(tags):
            tags_ = set([abjad_tags.NOT_MOL, abjad_tags.ONLY_MOL])
            return bool(set(tags) & tags_)

        deactivate: typing.Optional[callable_type]
        # then deactivate conflicting middle-of-line tags
        bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
        if bol_measure_numbers:
            nonmol_measure_numbers = bol_measure_numbers[:]
            final_measure_number = path.get_metadatum("final_measure_number")
            if final_measure_number is not None:
                nonmol_measure_numbers.append(final_measure_number + 1)
            nonmol_measure_numbers = [
                Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
            ]

            def deactivate(tags):
                if abjad_tags.NOT_MOL in tags:
                    if not bool(set(tags) & set(nonmol_measure_numbers)):
                        return True
                if abjad_tags.ONLY_MOL in tags:
                    if bool(set(tags) & set(nonmol_measure_numbers)):
                        return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "MOL"),
            deactivate=(deactivate, "conflicting MOL"),
            path=path,
            title="handling MOL tags ...",
        )

    @staticmethod
    def handle_shifted_clefs(path) -> "Job":
        """
        Handles shifted clefs.
        """

        def activate(tags):
            return abjad_tags.SHIFTED_CLEF in tags

        deactivate: typing.Optional[typing.Callable]
        # then deactivate shifted clefs at BOL:
        if path.is__segments():
            metadata_source = path.parent
        else:
            metadata_source = path
        string = "bol_measure_numbers"
        bol_measure_numbers = metadata_source.get_metadatum(string)
        if bol_measure_numbers:
            bol_measure_numbers = [Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

            def deactivate(tags):
                if abjad_tags.SHIFTED_CLEF not in tags:
                    return False
                if any(_ in tags for _ in bol_measure_numbers):
                    return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "shifted clef"),
            deactivate=(deactivate, "BOL clef"),
            path=path,
            title="handling shifted clefs ...",
        )

    @staticmethod
    def hide_default_clefs(path, undo=False) -> "Job":
        """
        Hides default clefs.
        """
        name = "default clef"

        def match(tags):
            tags_ = [abjad_tags.DEFAULT_CLEF]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(match, name), path=path, title="showing default clefs ...",
            )
        else:
            return Job(
                deactivate=(match, name), path=path, title="hiding default clefs ...",
            )

    @staticmethod
    def join_broken_spanners(path) -> "Job":
        """
        Joins broken spanners.
        """

        def activate(tags):
            tags_ = [abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
            return bool(set(tags) & set(tags_))

        def deactivate(tags):
            tags_ = [abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
            return bool(set(tags) & set(tags_))

        return Job(
            activate=(activate, "broken spanner expression"),
            deactivate=(deactivate, "broken spanner suppression"),
            path=path,
            title="joining broken spanners ...",
        )

    @staticmethod
    def show_clock_time_markup(path, undo=False) -> "Job":
        """
        Makes clock time markup job.
        """
        name = "clock time markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.CLOCK_TIME]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_figure_name_markup(path, undo=False) -> "Job":
        """
        Shows figure name markup.
        """
        name = "figure name markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.FIGURE_NAME]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_local_measure_number_markup(path, undo=False) -> "Job":
        """
        Shows local measure number markup.
        """
        name = "local measure number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.LOCAL_MEASURE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_measure_number_markup(path, undo=False) -> "Job":
        """
        Shows measure number markup.
        """
        name = "measure number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.MEASURE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_music_annotations(path, undo=False) -> "Job":
        """
        Shows music annotations.
        """
        name = "music annotation"

        def match(tags) -> bool:
            tags_ = abjad_tags.music_annotation_tags()
            return bool(set(tags) & set(tags_))

        def match_2(tags) -> bool:
            tags_ = [abjad_tags.INVISIBLE_MUSIC_COMMAND]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(match_2, name),
                deactivate=(match, name),
                path=path,
                title=f"hiding {name}s ...",
            )
        else:
            return Job(
                activate=(match, name),
                deactivate=(match_2, name),
                path=path,
                title=f"showing {name}s ...",
            )

    @staticmethod
    def show_spacing_markup(path, undo=False) -> "Job":
        """
        Shows spacing markup.
        """
        name = "spacing markup"

        def match(tags) -> bool:
            tags_ = abjad_tags.spacing_markup_tags()
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_tag(
        path,
        tag,
        *,
        match=None,
        prepend_empty_chord=None,
        skip_file_name=None,
        undo=False,
    ) -> "Job":
        """
        Shows tag.
        """
        if isinstance(tag, str):
            assert match is not None, repr(match)
        else:
            assert isinstance(tag, Tag), repr(tag)
        name = str(tag)

        if match is None:

            def match(tags) -> bool:
                tags_ = [tag]
                return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                prepend_empty_chord=prepend_empty_chord,
                skip_file_name=skip_file_name,
                title=f"hiding {name} tags ...",
            )
        else:
            return Job(
                activate=(match, name),
                path=path,
                skip_file_name=skip_file_name,
                title=f"showing {name} tags ...",
            )
