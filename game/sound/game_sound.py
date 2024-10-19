import pygame
import threading
from TTS.api import TTS
import queue
import torch

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TTS Player")

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Load TTS model (this might take some time)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device=device)

# Large body of text
large_text = """
### 1. **The Wysteria Kingdom**

**Location**: On a lush peninsula surrounded by the Elyrian Sea.
**Ruling Body**: The Monarchy of Wysteria, led by King Thayer III.
**Culture**: Known for grand architecture and vibrant marketplaces. Famous for their rich tapestries and woodwork.
**Primary Economic Activity**: Trade with nearby city-states through Elyria's Guilds, agriculture on the fertile peninsula.

- **Capital City:** Wysteria's Grandeur
  - **Architecture**: A blend of stone fortifications and ornate wooden palaces. The city is divided into sectors for merchants, artisans, and nobility.
  - **Layout**: Wide streets that lead to the central marketplace, home to exotic spices and textiles. The palace district contains the royal castle, surrounded by lush gardens and a famous music hall.
  - **Key Locations**:
    - **Temple of the Earth Mother**: A grand temple dedicated to the fertility goddess, located near the heart of the city.
    - **The Grand Market**: Where goods from all over Eridoria are bought and sold.
    - **Fortress Wyndor**: The royal castle and seat of government.

### 2. **Nefaria's Misty Haven**

**Location**: In a valley surrounded by towering mountains, where the air is misty and magical.
**Ruling Body**: Nefarian Brotherhood, governed by an anonymous council.
**Culture**: Emphasizes living in harmony with nature; crafts are woven from natural fibers and magic-infused wood.
**Primary Economic Activity**: Woodworking and weaving from unique materials found within their valley.

- **Settlement:** Misthaven
  - **Architecture**: Organic wooden buildings blend into the misty environment, with an emphasis on sustainability.
  - **Layout**: Narrow pathways wind through the settlement, reflecting the Nefarians' connection to nature. The central square hosts traditional dances and market stalls selling local crafts.
  - **Key Locations**:
    - **The Heartwood Tree**: A sacred tree believed to hold ancient secrets, surrounded by a serene glade for contemplation.
    - **The Weaver's Guild**: Where artisans weave magical fabrics that enhance the wearer's abilities.

### 3. **Celyddon's Greenhaven**

**Location**: In a valley where the air is crisp and clean, overlooking vast agricultural lands.
**Ruling Body**: The Council of Elders, chosen by the people for their wisdom in environmental matters.
**Culture**: Strong focus on sustainability and agriculture; crafts reflect harmony with nature.
**Primary Economic Activity**: Agriculture and trade of organic produce.

- **Settlement:** Greenhaven
  - **Architecture**: Buildings are crafted from natural materials, such as wood and earth. The town is organized into sectors for farming, craftsmanship, and living spaces.
  - **Layout**: Wide pathways lead through the settlement, with a central square that serves as a community center.
  - **Key Locations**:
    - **The Council Grove**: A sacred area where council meetings are held under ancient trees.
    - **The Great Farm**: Where innovative farming practices showcase Celyddon's commitment to sustainability.

### 4. **Vallara's Sunhaven**

**Location**: On a sun-kissed plateau overlooking the vast plains of Eridoria.
**Ruling Body**: The Enclave of Hidden Hands, governing through a network of influential figures.
**Culture**: Emphasizes light, knowledge, and strategic planning; crafts focus on illumination and astronomy.
**Primary Economic Activity**: Illumination magic, astronomy, and navigation tools.

- **Settlement:** Sunhaven
  - **Architecture**: Buildings are designed to maximize sunlight with intricate glasswork. The settlement is divided into sectors for scholars, artisans, and traders.
  - **Layout**: Wide streets lead to a central square that houses the great library of Vallara.
  - **Key Locations**:
    - **The Observatory**: A grand tower where astronomers study celestial movements and predict weather patterns.
    - **The Great Library**: A repository of ancient knowledge and magical texts.

### 5. **Aethoria's Whispering Isles**

**Location**: A series of floating islands above a sea of mist, said to be home to ethereal beings and ancient wisdom.
**Ruling Body**: The Archon, chosen for their spiritual guidance and wisdom.
**Culture**: Emphasizes spirituality, mysticism, and the harmony with nature; crafts are infused with magic for protection and healing.
**Primary Economic Activity**: Trade in magical goods and knowledge.

- **Settlements:** Whispering Isles
  - **Architecture**: Tightly-packed, intricately designed wooden buildings that seem to grow organically from the mist-shrouded sea.
  - **Layout**: Narrow pathways connect floating islands, leading to central markets and sacred sites.
  - **Key Locations**:
    - **The Archon's Sanctum**: A sacred site where the chosen leader resides and receives guidance from ethereal beings.
    - **The Celestial Market**: Where magical goods and knowledge are traded among the wise.

Each of these settlements reflects a unique aspect of Eridoria's diversity, showcasing how different cultures adapt to their environments while contributing to the rich tapestry of the world.
"""

# Chunk size (number of characters per chunk)
CHUNK_SIZE = 100

# Queue to hold audio chunks
audio_queue = queue.Queue()

# Flags
playing = False
stop_playback = False

def chunk_text(text, chunk_size):
    """
    Splits the text into chunks of approximately 'chunk_size' characters,
    ensuring that chunks end at sentence boundaries if possible.
    """
    import re
    sentences = re.split('(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def tts_worker(chunks):
    """
    Background thread to process text chunks and generate audio.
    """
    speaker = tts.speakers[0]
    global stop_playback
    for chunk in chunks:
        if stop_playback:
            break
        # Generate audio for the chunk
        wav = tts.tts(chunk,speaker=speaker,language='en')
        # Convert numpy array to sound and enqueue it
        sound = pygame.sndarray.make_sound((wav * 32767).astype('int16'))
        audio_queue.put(sound)

def play_audio():
    """
    Plays audio chunks from the queue.
    """
    global playing, stop_playback
    while playing and not audio_queue.empty():
        sound = audio_queue.get()
        channel = sound.play()
        while channel.get_busy():
            if stop_playback:
                channel.stop()
                break
            pygame.time.wait(100)
    playing = False

# Create buttons
font = pygame.font.SysFont(None, 36)
play_button = pygame.Rect(50, 100, 100, 50)
stop_button = pygame.Rect(250, 100, 100, 50)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, play_button)
    pygame.draw.rect(screen, GRAY, stop_button)

    play_text = font.render("Play", True, BLACK)
    stop_text = font.render("Stop", True, BLACK)
    screen.blit(play_text, (play_button.x + 20, play_button.y + 10))
    screen.blit(stop_text, (stop_button.x + 20, stop_button.y + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            stop_playback = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos) and not playing:
                # Start playing
                playing = True
                stop_playback = False
                # Chunk the text
                chunks = chunk_text(large_text, CHUNK_SIZE)
                # Start TTS worker thread
                tts_thread = threading.Thread(target=tts_worker, args=(chunks,))
                tts_thread.start()
                # Start playback
                play_thread = threading.Thread(target=play_audio)
                play_thread.start()
            elif stop_button.collidepoint(event.pos) and playing:
                # Stop playing
                stop_playback = True
                playing = False
                # Clear the audio queue
                with audio_queue.mutex:
                    audio_queue.queue.clear()
                pygame.mixer.stop()

    pygame.display.flip()
    pygame.time.wait(100)

pygame.quit()
