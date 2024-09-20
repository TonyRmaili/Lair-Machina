# from TTS.api import TTS

# # Initialize the model
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# # Convert text to speech and save it to a file
# tts.tts_to_file(text="Hello, welcome to TTS!", file_path="output.wav")


from pydub import AudioSegment

# Load audio and adjust speed
audio = AudioSegment.from_file("output1.wav")
faster_audio = audio.speedup(playback_speed=1.25)

# Export faster audio
faster_audio.export("output_fast1.wav", format="wav")


# from pydub import AudioSegment

# # Load the audio file with pydub
# audio = AudioSegment.from_wav("./output1.wav")

# # Speed up by 1.5x (150% of the original speed)
# new_speed = 1.1
# faster_audio = audio._spawn(audio.raw_data, overrides={
#      "frame_rate": int(audio.frame_rate * new_speed)
# }).set_frame_rate(audio.frame_rate)

# # Export the faster version to a new file
# faster_audio.export("./output_fast.wav", format="wav")

import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play background music (loop indefinitely)
pygame.mixer.music.load('C:/Users/harry/Documents/Lair-Machina/world_generator/The_journey(2).mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load and play the .wav file
output_file = "./output_fast1.wav"
voice_over = pygame.mixer.Sound(output_file)
voice_over.play()


pygame.mixer.music.set_volume(0.3)  # Set background music volume (0.0 to 1.0)
voice_over.set_volume(0.8)  # Set sound effect volume (0.0 to 1.0)

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

