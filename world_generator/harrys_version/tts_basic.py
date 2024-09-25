"""
example of simple TTS - text to speech- boilerplate

not sure if there are better less robot sounding - but it works for now

can change models -like Ollama it has some specific ones that it can run

ran:
pip install TTS

"""


from TTS.api import TTS

# Initialize the model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# # Convert text to speech and save it to a file
tts.tts_to_file(text="Hello, welcome to TTS!", file_path="output_test.wav")
