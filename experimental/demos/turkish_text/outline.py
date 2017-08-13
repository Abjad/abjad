import abjad
import os


input_text = u"""Taraf'ın Türkiye'nin saygın gazetelerinden olduğunun anımsatıldığı dilekçede."""
other = u"ÜÖ"
even_more_other = u"Ü"

vowel_treatments = {
     'a':   (2, abjad.NamedPitch("G4")),
     'i':   (2, abjad.NamedPitch("E4")),
    u'ı':   (1, abjad.NamedPitch("E4")),
     'u':   (2, abjad.NamedPitch("C4")),
    u'ü':   (4, abjad.NamedPitch("C4")),
     'e':   (2, abjad.NamedPitch("A3")),
     'o':   (2, abjad.NamedPitch("F3")),
    u'ö':   (4, abjad.NamedPitch("F3")),
}

def letter_to_duration_numerator(letter):
    letter = letter.lower()
    try:
        treatment_pair = consonant_treatments[letter]
    except KeyError:
        treatment_pair = vowel_treatments[letter]
    duration_numerator = treatment_pair[0]
    return duration_numerator

def letter_to_pitch(letter):
    letter = letter.lower()
    try:
        treatment_pair = consonant_treatments[letter]
    except KeyError:
        treatment_pair = vowel_treatments[letter]
    pitch = treatment_pair[-1]
    return pitch

consonant_treatments = {
    'b':    (2, abjad.NamedPitch("G4")),
    'c':    (3, abjad.NamedPitch("G4")),
   u'ç':    (3, abjad.NamedPitch("G4")),
    'd':    (2, abjad.NamedPitch("G4")),
    'f':    (3, abjad.NamedPitch("E4")),
    'g':    (2, abjad.NamedPitch("E4")),
   u'ğ':    (0, abjad.NamedPitch("E4")),
    'h':    (3, abjad.NamedPitch("E4")),
    'k':    (1, abjad.NamedPitch("C4")),
    'l':    (4, abjad.NamedPitch("C4")),
    'm':    (4, abjad.NamedPitch("C4")),
    'n':    (4, abjad.NamedPitch("C4")),
    'p':    (2, abjad.NamedPitch("A3")),
    'r':    (2, abjad.NamedPitch("A3")),
    's':    (4, abjad.NamedPitch("A3")),
   u'ş':    (4, abjad.NamedPitch("A3")),
    't':    (1, abjad.NamedPitch("A3")),
    'v':    (3, abjad.NamedPitch("F3")),
    'y':    (3, abjad.NamedPitch("F3")),
    'z':    (4, abjad.NamedPitch("F3")),
}


def preprocess_input_text(input_text):
    input_text = input_text.lower()
    result = []
    alphabet = list(consonant_treatments.keys()) + list(vowel_treatments.keys())
    permissible_characters = alphabet + [',', '.', ' ']
    for input_character in input_text:
        if input_character in permissible_characters:
            result.append(input_character)
    result = ''.join(result)
    return result

def count_vowels(word):
    vowel_count = 0
    for character in word:
        if character in vowel_treatments:
            vowel_count += 1
    return vowel_count

def count_consonants(word):
    consonant_count = 0
    for character in word:
        if character in consonant_treatments:
            consonant_count += 1
    return consonant_count

class WordAnalysis(object):

    def __init__(self, word):
        self.word = word
        self.word_length = len(word)
        self.vowel_count = 0
        self.consonant_count = 0
        self.vowel_pitches = []
        self.vowel_duration_numerators = []
        self.consonant_pitches = []
        self.consonant_duration_numerators = []
        self.analyze_word()

    def __repr__(self):
        return 'WordAnalysis({!r})'.format(self.word)

    def analyze_word(self):
        for character in self.word:
            if character in vowel_treatments:
                self.vowel_count += 1
                duration_numerator, pitch = vowel_treatments[character]
                self.vowel_duration_numerators.append(duration_numerator)
                self.vowel_pitches.append(pitch)
            elif character in consonant_treatments:
                duration_numerator, pitch = consonant_treatments[character]
                # account for silent g
                if duration_numerator:
                    self.consonant_count += 1
                    self.consonant_duration_numerators.append(duration_numerator)
                    self.consonant_pitches.append(pitch)
            else:
                raise ValueError('what is character {!r}?'.format(character))

def find_first_phrase(input_text):
    input_text = preprocess_input_text(input_text)
    first_phrase_index = min(input_text.find(','), input_text.find('.'))
    first_phrase = input_text[:first_phrase_index]
    return first_phrase

def analyze_phrase(phrase):
    phrase_words = phrase.split()
    word_analyses = []
    for phrase_word in phrase_words:
        word_analyses.append(WordAnalysis(phrase_word))
    return word_analyses

def make_lilypond_file(input_text, base_duration=Duration(1, 16)):
    first_phrase = find_first_phrase(input_text)
    word_analyses = analyze_phrase(first_phrase)
    upper_music, lower_music = make_music_for_word_analyses(word_analyses, base_duration)
    score_template = abjad.GroupedStavesScoreTemplate(staff_count=2)
    score = score_template()
    staff_1 = score['Staff 1']
    staff_2 = score['Staff 2']
    abjad.Clef('percussion')(staff_1)
    abjad.Clef('percussion')(staff_2)
    staff_1.extend(upper_music)
    staff_2.extend(lower_music)

    abjad.override(staff_1).staff_symbol.line_count = 4
    abjad.override(staff_2).staff_symbol.line_count = 4

    lilypond_file = lilypondfiletools.LilyPondFile.new(score)
    format_score(score)
    format_lilypond_file(lilypond_file)
    return lilypond_file

def format_score(score):
    abjad.override(score).bar_line.transparent = True
    abjad.override(score).beam.positions = (-6, -6)
    abjad.override(score).spacing_spanner.strict_grace_spacing = True
    abjad.override(score).spacing_spanner.strict_note_spacing = True
    abjad.override(score).spacing_spanner.uniform_stretching = True
    abjad.override(score).span_bar.transparent = True
    abjad.override(score).stem.direction = 'down'
    abjad.override(score).time_signature.transparent = True
    abjad.setting(score).autoBeaming = False
    abjad.setting(score).proportionalNotationDuration = schemetools.SchemeMoment((1, 64))
    abjad.setting(score).tupletFullLength = True

    vector = schemetools.make_spacing_vector(0, 0, 6, 0)
    abjad.override(score[0]).staff_grouper.staff_staff_spacing = vector

    return score

def format_lilypond_file(lilypond_file):
    lilypond_file.global_staff_size = 14
    lilypond_file.header_block.title = abjad.Markup('Turkish text')
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    vector = schemetools.make_spacing_vector(0, 0, 12, 0)
    lilypond_file.paper_block.markup_system_spacing = vector
    lilypond_file.paper_block.top_margin = 10
    return lilypond_file

def make_music_for_word_analyses(word_analyses, base_duration):
    vowel_counts = [x.vowel_count for x in word_analyses]
    upper_durations = [base_duration * x for x in vowel_counts]
    lower_durations = abjad.rotate_sequence(upper_durations, -1)
    upper_pitches = [x.vowel_pitches for x in word_analyses]
    lower_pitches = [x.consonant_pitches for x in word_analyses]
    upper_proportions = [x.vowel_duration_numerators for x in word_analyses]
    lower_proportions = [x.consonant_duration_numerators for x in word_analyses]
    upper_music = make_tuplets(upper_durations, upper_proportions, upper_pitches)
    lower_music = make_tuplets(lower_durations, lower_proportions, lower_pitches)
    return upper_music, lower_music

def make_tuplets(durations, proportions, pitch_lists):
    tuplets = []
    for duration, proportion, pitch_list in zip(
        durations, proportions, pitch_lists):
        tuplet = abjad.Tuplet.from_duration_and_ratio(duration, proportion)
        spannertools.Beam(tuplet)
        for leaf, pitch in zip(tuplet.leaves, pitch_list):
            leaf.written_pitch = pitch
        tuplets.append(tuplet)
    return tuplets


if __name__ == '__main__':
    os.system('clear')
    lilypond_file = make_lilypond_file(input_text)
    show(lilypond_file)
