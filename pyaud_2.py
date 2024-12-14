import numpy as np
import matplotlib.pyplot as plt
import pygame
from mido import MidiFile

# Convert MIDI note number to frequency
def midi_to_hz(midi_note):
    A4 = 440.0
    return A4 * 2 ** ((midi_note - 69) / 12.0)

# Function to extract MIDI notes and timings from the MIDI file
def extract_midi_notes(midi_file):
    mid = MidiFile(midi_file)
    notes = []
    times = []
    
    # Iterate through all the MIDI tracks to extract note events
    current_time = 0
    for i, track in enumerate(mid.tracks):
        for msg in track:
            current_time += msg.time  # Accumulate time
            if msg.type == 'note_on':
                notes.append(msg.note)  # MIDI note number
                times.append(current_time / mid.ticks_per_beat)  # Convert time to seconds
                
    return times, notes

# Function to generate the circular visualization with spikes based on MIDI notes
def generate_spike_circle_with_midi(midi_file):
    # Initialize pygame mixer for audio playback
    pygame.mixer.init(frequency=22050)
    
    # Extract notes and timings from MIDI file
    times, notes = extract_midi_notes(midi_file)
    
    # Convert MIDI notes to frequencies
    frequencies = [midi_to_hz(note) for note in notes]
    
    # Calculate the duration based on the last note's time
    duration = times[-1] if times else 0
    
    # The circumference of the circle will be equal to the duration of the MIDI (1 cm per second)
    circumference = duration * 1  # 1 cm per second
    radius = circumference / (2 * np.pi)  # Calculate the radius
    
    # Create angular positions corresponding to the time positions
    theta = np.linspace(0, 2 * np.pi, len(times))  # Angular positions for each second of audio
    
    # Create a polar plot for circular visualization
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    ax.set_title('Circular Visualization of MIDI Notes', fontsize=14, color='black', weight='bold')
    
    # Base circle (circle outline)
    ax.plot(theta, np.full_like(theta, radius), color='black', linewidth=2)
    
    # Create spikes along the circumference based on frequencies
    for i, frequency in enumerate(frequencies):
        angle = theta[i]
        
        # Skip silent frequencies (0 Hz)
        if frequency == 0:
            continue
        
        # Map frequencies to spike length (directly proportional to frequency)
        spike_length = np.log(frequency + 1) * 0.5  # Log scale to make spikes more reasonable
        
        # Assign colors based on the frequency using a vibrant colormap
        color = plt.cm.plasma(frequency / np.max(frequencies))  # Using 'plasma' colormap for vibrant colors
        
        # Plot a spike at this angle with color
        ax.plot([angle, angle], [radius, radius + spike_length], color=color, lw=5)  # Increase line width (lw=5)
    
    # Add the message before the visualization
    print("Can't find sheet music for that song you love? Here's a visualization of it, good luck!")
    
    # Start the audio playback
    pygame.mixer.music.load(midi_file)
    pygame.mixer.music.play()
    
    # Show the visualization
    plt.show()

# Example Usage:
# Provide the path to your MIDI file
midi_file = r"C:\path\to\your\midi\file.mid"
generate_spike_circle_with_midi(midi_file)
