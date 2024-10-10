# ZULU

### Description
Zulu is an **open-source**, **private** alternative to popular voice assistants like Alexa. However, Zulu is not a "smart assistant." Unlike other assistants that record and store your voice data to sell to advertisers, Zulu prioritizes your privacy. It doesn't store your conversations, ensuring a safer and more private experience.

### Features:
- Listens for a user-defined wake word (set in `wakeword.txt`).
- Voice commands are processed using `spacy` for natural language understanding.
- Anonomously Uses Googles `SpeechRecognition` for voice input and `pyttsx3` for text-to-speech output. (Plans to update to offline speech recognition in future)
- No voice data is recorded or sold – Zulu simply listens and responds accordingly, nothing more.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jtanner5674/ZULU.git
   cd ZULU
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the Spacy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

### Usage

1. Configure the wake word in `wakeword.txt`:
   ```
   zulu, True
   ```
   Change "zulu" to your preferred wake word.

2. Run the main script:
   ```bash
   python Zulu.py
   ```

3. Zulu will now listen for your wake word and execute commands accordingly.

### Requirements

- `SpeechRecognition`
- `pyttsx3`
- `spacy`

---

Let me know if you'd like further adjustments!
