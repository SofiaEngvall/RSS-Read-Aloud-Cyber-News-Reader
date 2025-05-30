# RSS Read Aloud for Cyber Security News


rss-read-aloud.py - RSS feed reader with AI summarization<br/>
version 1.0<br/>
by Sofia Engvall - FixIt42, 2025-05-04<br/>
<br/>
This script fetches articles from a list of RSS feeds, summarizes them using AI (ollama using llama3.2), and reads them aloud.<br/>
<br/>
The script is designed to be run in a terminal but as most output is spoken, it should work in a GUI as well.


### To run in a virtual environment

To keep installations of different scripts separate we run then in virtual environments. These have their own set of installed libraries.

Install
```sh
sudo apt install pypy3-venv
python3 -m venv .
```

Start
```sh
source bin/activate
```

Stop
```sh
deactivate
```

For details:<br/>
https://www.fixit42.com/notes/programming/python/python-course/the-python-virtual-environment.html

### Windows Installation

Windows has it's own built in tts so we don't need to install one or use the internet for this.<br/>

Clone the repo = Download the files:
```sh
git clone https://github.com/SofiaEngvall/RSS-Read-Aloud-Cyber-News-Reader.git
```

Install libraries:
```sh
pip install -r requirements-windows.txt
```

### Linux Installation


Please observe that the Linus version uses gTTS which means it sends the article to goole for tts. The resulting audio is played using ffmpeg.<br/>

Clone the repo = Download the files:
```sh
git clone https://github.com/SofiaEngvall/RSS-Read-Aloud-Cyber-News-Reader.git
```

Install ffmpeg:
```sh
sudo apt install ffmpeg python3-pyaudio portaudio19-dev python3-dev
```

Install libraries:
```sh
pip3 install -r requirements-linux.txt
```


### Script Settings
- `use_ollama = True` If True, use Ollama for summarization. If False, just read the full articles, even if they are thousands of words long.
- `START_OLLAMA = True` If True, start Ollama if it is not running. If False, ask the user if they want to start it.
- `OLLAMA_PATH = "D:/ollama/ollama.exe"` The full path to the ollama executable file. Use double backslashes or single forward slashes.
- `DEFAULT_TTS_SPEED = 4` The default speed of the text-to-speech voice. -10 to 10, where 0 is normal speed.
- `DEFAULT_STT_RETRIES = 0`  -1 = no question asked, 0 = ask once, 1 = retry once, 2 = retry twice, etc.
- `DEFAULT_ARTICLE_DAYS = 7` How old articles to read, older ones are skipped
- `DEFAULT_ARTICLE_LENGTH = 400` Default length of the long article summary. Articles 100 words longer are read in full.
- `ALWAYS_READ_LONG = True`  if True, always read the long summary and will skip making a short summary
- `use_playwright = True` If true, use Microsoft Playwright to access anti-scraping web pages


### RSS feeds
- Please tell me if you have more feeds to add something is incorrect or missing so I can fix it!
- The list was refined and formatted with the help of AI so please tell me errors I missed, like a bad description.


### TODO! Features to add!
- Add functionality to save and load (file? registry?) information, for example:
  - Read articles - to remember what you already read/heard
  - RSS feed list
  - Ollama path
  - Article length
  - Article days
- Possible add command line options to set these values, overriding both the defaults in the script and the saved options
- Make a database of articles
- Make a database for the RSS feeds, or just add more fields to the list
- Add feedback on the feeds - Maybe at the end of the reading of a feed - connect to db on the web server?
  - Then maybe host a db for feeds there too - then just sync at start
- Make main fit on one page

### Used libraries
<br/>
- `os` to get terminal size
- `subprocess` to start Ollama
- `sys` to find the python executable running this script to use when installing ms playwright
<br/>
- `time` and `datetime` to manage time and timezones
- `dateutil.parser` to parse dates
<br/>
- `feedparser` to parse RSS feeds
- `requests` to download articles
- `playwright` to bypass restrictions on some webpages
- `webbrowser` to open links in a browser
- `readability-lxml` (and `lxml_html_clean`) to extract the main content from webpages
- `BeautifulSoup` to convert HTML to plain text
<br/>
- `ollama` for AI summarization
<br/>
- `speaker` and `listener` modules for text-to-speech and speech recognition
  (These modules will be available in the same directory as this script.)
<br/>
