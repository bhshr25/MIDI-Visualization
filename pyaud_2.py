import numpy as np
import matplotlib.pyplot as plt
import pygame
from mido import MidiFile

# midi note numbers to frequency
def midi_to_hz(midi_note):
    A4 = 440.0
    return A4 * 2 ** ((midi_note - 69) / 12.0)

# extracting notes and timestamps from tracks
def extract_midi_notes(midi_file):
    mid = MidiFile(midi_file)
    notes = []
    times = []

    current_time = 0
    for track in mid.tracks:
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(msg.note)
                times.append(current_time / mid.ticks_per_beat)

    return times, notes

# plot generation (circular with spikes)
def generate_spike_circle_with_midi(midi_file):
    # Frequency is set 
    pygame.mixer.init(frequency=22050)

    times, notes = extract_midi_notes(midi_file)
    if not notes:
        print("No notes found in the MIDI file.")
        return
    # note to frequency using formula
    frequencies = [midi_to_hz(note) for note in notes]

    # normalisation process
    min_freq = min(frequencies)
    max_freq = max(frequencies)

    # generates equal thetas between 0 and 2 pi using numpy
    theta = np.linspace(0, 2 * np.pi, len(times))
    radius = 5  # this is the base radius

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8)) #to set polar plot instead of cartesian
    ax.set_title('Circular Visualization of MIDI Notes', fontsize=14, color='black', weight='bold')
    ax.plot(theta, np.full_like(theta, radius), color='black', linewidth=2)  # base circle np.full_like creates an array with same shape and size as theta but values of radius

    # Draw spikes
    for i, freq in enumerate(frequencies):
        if freq == 0:
            continue

        angle = theta[i]
        norm_freq = (freq - min_freq) / (max_freq - min_freq)
        spike_length = norm_freq * radius * 0.8  

        color = plt.cm.plasma(norm_freq)  # colourmap plasma for yellow and purple
        ax.plot([angle, angle], [radius, radius + spike_length], color=color, lw=5) 

    print("Can't find sheet music for that song you love? Here's a visualization of it, good luck!")

    # to play midi audio
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()

    # visualisation
    plt.show()
# === USAGE ===
midi_file = r"C:\path\to\your\midi\file.mid"  # 🔁 Change this to your MIDI path
generate_spike_circle_with_midi(midi_file)
