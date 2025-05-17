import numpy as np
import matplotlib.pyplot as plt
import pygame
from mido import MidiFile

# Convert MIDI note number to frequency (in Hz)
def midi_to_hz(midi_note):
    A4 = 440.0
    return A4 * 2 ** ((midi_note - 69) / 12.0)

# Extract MIDI note events and their timestamps
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

# Generate circular spike plot from MIDI file
def generate_spike_circle_with_midi(midi_file):
    # Audio playback
    pygame.mixer.init(frequency=22050)
    
    # Get notes and timestamps
    times, notes = extract_midi_notes(midi_file)
    if not notes:
        print("No notes found in the MIDI file.")
        return

    frequencies = [midi_to_hz(note) for note in notes]

    # Normalize frequency for spike height
    min_freq = min(frequencies)
    max_freq = max(frequencies)

    # Generate angular positions for each note
    theta = np.linspace(0, 2 * np.pi, len(times))
    radius = 5  # Fixed base radius for consistent appearance

    # Set up polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.set_title('Circular Visualization of MIDI Notes', fontsize=14, color='black', weight='bold')
    ax.plot(theta, np.full_like(theta, radius), color='black', linewidth=2)  # base circle

    # Draw spikes
    for i, freq in enumerate(frequencies):
        if freq == 0:
            continue

        angle = theta[i]
        norm_freq = (freq - min_freq) / (max_freq - min_freq)
        spike_length = norm_freq * radius * 0.8  # Up to 80% of the base radius

        color = plt.cm.plasma(norm_freq)  # Vibrant colormap
        ax.plot([angle, angle], [radius, radius + spike_length], color=color, lw=5)

    print("Can't find sheet music for that song you love? Here's a visualization of it, good luck!")

    # Play MIDI audio
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()

    # Show visualization
    plt.show()

# === USAGE ===
midi_file = r"C:\path\to\your\midi\file.mid"  # 🔁 Change this to your MIDI path
generate_spike_circle_with_midi(midi_file)
