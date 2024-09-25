"""
Example of workflow/pipeline/whatever where you ask the LLM to generate a text
turn the output into speech with TTS
(optional - speed it up with pydub - (pip install pydub))
and play it with pygame (pip install pygame)


---problem is the server doesnt have a sound thing (or it does and stuff gets played at gabriels (even worse)) - so it is impossible to know if it really works as is (can still check the sound files ofc)
"""




##################### create wav with TTS from text#################
# from TTS.api import TTS

# # Initialize the model
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# # Convert text to speech and save it to a file
# tts.tts_to_file(text="Hello, welcome to TTS!", file_path="output.wav")




##################change speed of wav (usually the text is very slow to listen to)######################
from pydub import AudioSegment

# Load audio and adjust speed
audio = AudioSegment.from_file("output2.wav")
faster_audio = audio.speedup(playback_speed=1.25)

# Export faster audio
faster_audio.export("output_fast2.wav", format="wav")




##################use pygame to play voice TTS clip and generated backgroundmusic (uses test from loudme.ai - look at options later)###############
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play background music (loop indefinitely)
pygame.mixer.music.load('./The_journey(2).mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely (should be while voice plays not infinite, or well should be infinite as we port the whole game to run on pygame)

# Load and play the .wav file
output_file = "./output_fast2.wav"
voice_over = pygame.mixer.Sound(output_file)
voice_over.play()


pygame.mixer.music.set_volume(0.3)  # Set background music volume (0.0 to 1.0)
voice_over.set_volume(0.8)  # Set sound effect volume (0.0 to 1.0)

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

