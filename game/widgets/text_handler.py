import re


class TextHandler:
    def __init__(self,text):
        self.text = text

    def split_sentences(self):
    # Split the string by period and remove any leading/trailing whitespace
        sentences = [sentence.strip() for sentence in self.text.split('.') if sentence.strip()]
        
        return sentences
    
    def clean_text(self):
        # Remove unwanted symbols (*, **, ###, etc.)
        cleaned_text = re.sub(r'[^\w\s.,;:!?\'"-]', '', self.text)

        # Remove multiple spaces and replace with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        # Ensure proper spacing around punctuation
        cleaned_text = re.sub(r'\s([?.!,;:"](?:\s|$))', r'\1', cleaned_text)

        self.text = cleaned_text
        
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


    text_handler = TextHandler(text=large_text)
    text_handler.clean_text()
    sentances =text_handler.split_sentences()
    print(sentances)
    # text_handler.split_sentences()