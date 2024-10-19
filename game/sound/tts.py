from TTS.api import TTS
import sounddevice as sd
import torch
import time
import sys



class TTSGame:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        self.speakers = self.tts.speakers
        self.speaker = self.speakers[0]

    def play_wav(self,sample,emotion=None,rate=22050):
        wav = self.tts.tts(text=sample, language="en", speaker=self.speaker,emotion=emotion)
        sd.play(wav, samplerate=rate)
        sd.wait()

    def streaming(self,sentances):
        for sentance in sentances:
            print(sentance)
            self.play_wav(sample=sentance)


    def save_wav(self,sample,path):
        wav = self.tts.tts_to_file(text=sample,speaker=self.speaker,language='en',file_path=path)
        return wav

    def list_speakers(self):
        print(f'Speakers count: {len(self.speakers)}')
        for i, speaker in enumerate(self.speakers):
            print(f'{i}: {speaker}')

    def change_speaker(self, speaker_index: int):
        if 0 <= speaker_index < len(self.speakers):
            self.speaker = self.speakers[speaker_index]
            print(f'Speaker changed to: {self.speaker}')
        else:
            print(f'Invalid speaker index. Please select a number between 0 and {len(self.speakers) - 1}.')

    def run(self):
        while True:
            print("\n--- TTS Game Menu ---")
            print("1. List available speakers")
            print("2. Select a speaker")
            print("3. Input text for TTS")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.list_speakers()
            elif choice == '2':
                try:
                    speaker_index = int(input("Enter the speaker index: "))
                    self.change_speaker(speaker_index)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '3':
                sample = input("Enter the text you want to synthesize: ")
                print("Generating speech...")
                self.play_wav(sample)
            elif choice == '4':
                print("Exiting TTS Game.")
                sys.exit()
            else:
                print("Invalid option. Please select 1, 2, 3, or 4.")


if __name__=='__main__':
    large_text = '''
In the high-fantasy world of Eridoria, several key organizations, guilds, and secret societies play significant roles in shaping its political and social landscape.

### 1. **The Council of Sages** (Elyria):
- **Goal**: To advance knowledge and understanding of the natural world.
- **Leadership**: Led by an elected chair from among its senior members.
- **Alliances**: Supports the Elyrian Guilds in their quest for knowledge and resources. Collaborates with Vallara's Order of Scholars to promote trade and exchange of ideas.
- **Conflicts**: Sometimes at odds with Celyddon's Order of the Green Hand, as their environmental focus can be seen as a limitation on scientific progress.

### 2. **The Guilds of Elyria** (Elyria):
- **Goal**: To protect and advance Elyrian trade, commerce, and industry.
- **Leadership**: Directed by an executive board elected from among the guild leaders.
- **Alliances**: Partners with Vallara's Merchants' Association in joint ventures. Supports Celyddon's city-states through trade agreements.
- **Conflicts**: Engages in a delicate balance of power against the interests of Nefaria, which seeks to disrupt Elyrian control over key resources.

### 3. **The Order of the Silver Oak** (Aethoria):
- **Goal**: To protect and preserve the natural world, advocating for harmony with nature.
- **Leadership**: Led by an Archon chosen through a sacred ceremony among Aethorians.
- **Alliances**: Maintains close relations with Celyddon's Order of the Green Hand. Works to maintain balance within Vallara between agricultural interests and environmental protection.
- **Conflicts**: At times, finds itself in conflict with Elyria's Guilds over issues related to resource exploitation.

### 4. **The Nefarian Brotherhood** (Nefaria):
- **Goal**: To protect the wilderness and its inhabitants from encroaching settlements and exploiters.
- **Leadership**: Governed by a mysterious council that advises on matters of survival and protection.
- **Alliances**: Engages in clandestine operations against Elyrian guilds and Vallara's agricultural interests, viewing them as threats to Nefaria's way of life.
- **Conflicts**: Has longstanding conflicts with Celyddon over land rights and resource management.

### 5. **The Order of the Green Hand** (Celyddon):
- **Goal**: To balance nature and human settlements, promoting sustainability and ecological harmony.
- **Leadership**: Led by a council chosen through consensus among its members.
- **Alliances**: Allies with Aethoria's Order of the Silver Oak to protect natural habitats. Negotiates trade agreements with Elyria and Vallara.
- **Conflicts**: Faces challenges from Nefaria over land use policies, as well as from factions within Celyddon that prioritize economic growth over environmental protection.

### 6. **The Enclave of Hidden Hands** (Vallara):
- **Goal**: To secretly protect the balance of power and interests within Vallara.
- **Leadership**: Governed by an anonymous council believed to include influential figures from each city-state.
- **Alliances**: Works behind the scenes with Aethoria's Order of the Silver Oak on matters of mutual interest. Influences decisions in Celyddon regarding trade and environmental protection.
- **Conflicts**: Engages in covert operations against elements within Vallara that seek to disrupt the balance between city-states.

These organizations play significant roles in shaping the political, social, and economic landscapes across Eridoria, each with its unique goals, interests, and interactions. Their influence is felt throughout major events, settlements, and power structures, contributing to a rich tapestry of conflict and cooperation that underpins life in this high-fantasy world.
'''


    start_time = time.time()
    tts = TTSGame()
    tts.save_wav()
    # tts.streaming(text=large_text)
    # tts.run()
    # tts.play_wav(sample=large_text)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Script runtime: {execution_time} seconds")

    # pygame.init()
    # pygame.mixer.init(frequency=22050, size=-16, channels=2)
    # pygame.mixer.music.load('The_journey(2).mp3')
    # pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    # pygame.mixer.music.set_volume(0)  # Set background music volume (0.0 to 1.0)