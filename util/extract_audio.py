import sys
from moviepy.editor import *
from glob import glob
import os


def wmv_to_wav(entry):
    video = VideoFileClip(entry)
    #extract audio from video
    audio = video.audio
    #write audio file with specified ending .wav
    filename = os.path.basename(entry)
    filename = filename.replace(' ', '_')
    filename = filename.replace('-', '_')
    filename = filename.replace('.', '_')
    filename = filename.replace('__', '_')
    filename = filename.replace('___', '_')
    filename = filename[:-4] + '.wav'
    #filename = filename[:-4]+'.wav'
    #filename = filename[:10] + '_' + filename[-9:]
    audio.write_audiofile('./audio/' +filename)

def mp4_to_wav(entry):
    video = VideoFileClip(entry)
    #extract audio from video
    audio = video.audio
    #write audio file with specified ending .wav
    filename = os.path.basename(entry)
    filename = filename.replace(' ', '_')
    filename = filename.replace('-', '_')
    filename = filename.replace('.', '_')
    filename = filename.replace('__', '_')
    filename = filename.replace('___', '_')
    filename = filename[:-4] + '.wav'
    #filename = filename[:-4]+'.wav'
    #filename = filename[:10] + '_' + filename[-9:]
    audio.write_audiofile('./audio/' +filename)


#Sources:
# - https://zulko.github.io/moviepy/
# - https://medium.com/@steadylearner/how-to-extract-audio-from-the-video-with-python-aea325f434b6
