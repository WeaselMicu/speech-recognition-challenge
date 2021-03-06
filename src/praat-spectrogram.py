#!/usr/bin/env python3

# Program: praat-spectrogram.py
# Purpose: Create detailed spectrograms using Praat

from shutil import rmtree
import glob
import matplotlib.pyplot as plt
import numpy as np
import os.path
import parselmouth

# Spectrogram functions
def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values.T)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_intensity(intensity):
    plt.plot(intensity.xs(), intensity.values, linewidth=3, color='w')
    plt.plot(intensity.xs(), intensity.values, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")

# Create output directories
commands = ["down", "go", "left", "no", "off", "right", "stop", "up", "yes"]
for c in commands:
    if os.path.isdir(os.path.join("../train", c)):
        rmtree(os.path.join("../train", c))
    os.makedirs(os.path.join("../train", c))
    
    if os.path.isdir(os.path.join("../validation", c)):
        rmtree(os.path.join("../validation", c))
    os.makedirs(os.path.join("../validation", c))

# Create spectrograms
for c in commands:
  for wave_file in glob.glob("../data/train/audio/%s/*.wav" % c):
      snd = parselmouth.Sound(wave_file)
      snd.pre_emphasize()
      
      intensity = snd.to_intensity()
      spectrogram = snd.to_spectrogram()
      
      if np.random.uniform(1, 100) <= 15:
          dest = "validation"
      else:
          dest = "train"
          
      output_file = wave_file.replace("../data/train/audio/", "")\
          .replace("wav", "png")
      
      plt.figure()
      draw_spectrogram(spectrogram)
      plt.twinx()
      draw_intensity(intensity)
      plt.xlim([0, 1])
      plt.savefig(os.path.join("..", dest, output_file))
      plt.close()
      plt.clf()
      plt.cla()
