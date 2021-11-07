import os

import connexion

import random
import time
from pathlib import Path
import pygame
from pygame.locals import *

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

# Read the swagger.yml file to configure the endpoints
# connex_app.add_api("swagger.yml")

pygame.init()

#in the folder where the audio files are, there are 150 audio files

sounds = { #'evil_girl' : r'08-Free_Sounds-Evil_Girl.wav',
           'werewolf' : r'02-FreeSounds-Werewolf.wav',
           'laughhowl1':'laughhowl1.wav',
           'wickedmalelaugh1':'wickedmalelaugh1.wav',
           'ghostly2' : 'ghostly2.wav',
           'scream15' : '14-Free-Scream_14.wav'}
playlist = { 'drone_one' : r'09-Free_Sounds-Creepy_Drone_1.mp3', 
             'drone_two' : r'10-Free_Sounds-Creepy_Drone_2.mp3'}
pygame.mixer.init()


@connex_app.route("/sound")
@connex_app.route("/sound/<string:sound_file_name>")
def sound(sound_file_name=""):

    if sound_file_name:
        sound = pygame.mixer.Sound(sounds[sound_file_name])
    else:
        sound = pygame.mixer.Sound(random.choice(list(sounds.values())))
    sound.set_volume(.5)
    sound.play()

    return ""

@connex_app.route("/music")
@connex_app.route("/music/<string:music_file_name>")
def music(music_file_name=""):

    if music_file_name:
        pygame.mixer.music.load(playlist[music_file_name])
    else:
        pygame.mixer.music.load(random.choice(list(playlist.values())))

    pygame.mixer.music.play(loops=1, fade_ms=30 * 1000)


    return ""

if __name__ == "__main__":
    connex_app.run(debug=True, port=5001)
