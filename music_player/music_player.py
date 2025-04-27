import os
from music21 import scale, pitch, tempo
from music21.note import Note
from music21.pitch import Pitch
from music21.stream import Stream
from cellular_automata.cellular_automata import CellularAutomata
import subprocess
from collections import namedtuple
import numpy as np

SOUNDFONT_PATH = "music_player/soundfont.sf2"
MIDI_PATH = "temp/midi_file.mid"
WAV_PATH = "temp/wav_file.wav"

Segment = namedtuple("Segment", ["pitch", "start", "length"])

MAJOR_PENTATONIC_STRINGS = [
    "F#3",
    "G#3",
    "A#3",
    "C#3",
    "D#3",
    "F#4",
    "G#4",
    "A#4",
    "C#4",
    "D#4",
    "F#5",
    "G#5",
    "A#5",
    "C#5",
    "D#5",
]


def create_segments(binary_list, pitch):
    running_count = 0
    segments = []

    for i, bit in enumerate(binary_list):
        if bit == 1:
            running_count += 1
        else:
            if running_count > 0:
                segments.append(
                    Segment(
                        pitch=pitch, start=(i - running_count), length=running_count
                    )
                )
                running_count = 0

    if running_count > 0:
        segments.append(Segment(pitch=pitch, start=i, length=running_count))

    return segments


class MusicPlayer:
    def __init__(self, automata: CellularAutomata):
        self.history = np.array(automata.get_history())
        self.stream = self.generate_stream()

    def generate_stream(self):
        song = Stream()

        song.insert(0, tempo.MetronomeMark(number=180))

        pitches = [Pitch(n) for n in MAJOR_PENTATONIC_STRINGS]

        start = (len(self.history.T) - len(MAJOR_PENTATONIC_STRINGS)) // 2
        end = start + len(MAJOR_PENTATONIC_STRINGS)

        for i, col in enumerate(self.history.T):
            if i < start or i >= end:
                continue

            pitch = pitches[i % len(MAJOR_PENTATONIC_STRINGS)]
            segments = create_segments(col, pitch)

            for segment in segments:
                note = Note(segment.pitch, quarterLength=segment.length)
                song.insert(segment.start, note)

        return song

    def export_as_mp3(self, output_dir):
        self.stream.write("midi", fp=MIDI_PATH)

        subprocess.run(
            [
                "fluidsynth",
                "-ni",
                SOUNDFONT_PATH,
                MIDI_PATH,
                "-F",
                WAV_PATH,
                "-r",
                "44100",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        output_path = os.path.join(output_dir, "song.mp3")

        subprocess.run(
            ["ffmpeg", "-y", "-i", WAV_PATH, output_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        return output_path
