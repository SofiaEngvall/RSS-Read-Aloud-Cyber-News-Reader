#!/usr/bin/env python3

# rss-read-aloud.py - RSS feed reader with AI summarization
# version 1.0
# by Sofia Engvall - FixIt42, 2025-05-04
# https://github.com/SofiaEngvall/RSS-Read-Aloud-Cyber-News-Reader.git

# This script fetches articles from a list of RSS feeds, summarizes them using AI (Ollama), and reads them aloud.
# Library list in the README.md
# The script is designed to be run in a terminal but as most output is spoken, it should work in a GUI as well.


### Import libraries
import os
import subprocess
import sys

import time
from datetime import datetime, timezone
from dateutil import parser

import feedparser
import requests
from playwright.sync_api import sync_playwright, TimeoutError
from webbrowser import open_new_tab
from readability import Document
from bs4 import BeautifulSoup

import ollama

import speaker
import listener
from rss_feed_list import rss_feeds


# TODO! Features to add!
# - Add Linus TTS - possibly using gtts, suggestions are welcome
# - Add functionality to save and load (file? registry?) information, for example:
#   - Read articles - to remember what you already read/heard
#   - RSS feed list
#   - Ollama path
#   - Article length
#   - Article days
#   - The main article - makes it possible to later search articles! Also useful for multi-user
# - Possible add command line options to set these values, overriding both the defaults in the script and the saved options
# - Make a database of articles
# - Make a database for the RSS feeds, or just add more fields to the list
# - Add feedback on the feeds - Maybe at the end of the reading of a feed - connect to db on the web server?
#   - Then maybe host a db for feeds there too - then just sync at start
# - Make main fit on one page


### Settings
use_ollama = True #If True, use Ollama for summarization. If False, just read the full articles, even if they are thousands of words long.
START_OLLAMA = True #If True, start Ollama if it is not running. If False, ask the user if they want to start it.
#OLLAMA_PATH = "/opt/ollama/bin/ollama" #The full path to the ollama executable file. Use double backslashes or single forward slashes.
OLLAMA_PATH = "d:/ollama/ollama.exe" #The full path to the ollama executable file. Use double backslashes or single forward slashes.
DEFAULT_TTS_SPEED = 2 #4 #The default speed of the text-to-speech voice. -10 to 10, where 0 is normal speed.
DEFAULT_STT_RETRIES = -1 # -1 = no question asked, 0 = ask once, 1 = retry once, 2 = retry twice, etc. -1 is useful if you don't have a mic.
DEFAULT_ARTICLE_DAYS = 7 #How old articles to read, older ones are skipped
#GIVE_UP_AFTER_N_OLD = 3 # TODO!
#old_articles = 0
DEFAULT_ARTICLE_LENGTH = 500 #Default length of the long article summary. Articles 100 words longer are read in full.
ALWAYS_READ_LONG = True # if True, always read the long summary and will skip making a short summary
use_playwright = True #If true, use Microsoft Playwright to access anti-scraping web pages

# ### File store settings and variables
# use_file_store = True
# FILE_STORE_PATH = "d:/articles/"

# def init_file_store():
#     if not os.path.isdir(FILE_STORE_PATH):
#         try:
#             os.mkdirs(FILE_STORE_PATH)
#             print(f"File store created successfully.")
#         except FileExistsError:
#             print(f"File store already exists.")
#         except PermissionError:
#             print(f"Permission denied: Unable to create File store.")
#         except Exception as e:
#             print(f"An error occurred wgile creating file store: {e}")

### Headers for the requests - Used to mimic a real browser request and avoid being blocked
headers = {
    #"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    'Te': 'trailers',
    'Connection': 'keep-alive',
}

### Function to print a dashed line
def dash_line():
    print("-" * max(0, (os.get_terminal_size().columns-1))) #------------------------------------------

### Function to print the keys of the first entry in the feed
def print_key_names(feed):
    if feed.entries:
        entry = feed.entries[0]
        for key in entry.keys():
            print(f"{key}, ", end="")

### Function to get the feed entries from a given RSS feed
def get_feed_entries(rss_feed):
    feed = feedparser.parse(rss_feed)
    dash_line() #------------------------------------------
    if feed.entries:
        if "title" in feed.feed:
            s.speak(f"\nFetched {len(feed.entries)} articles from {feed.feed.title}.\n")
        else:
            s.speak(f"\nFetched {len(feed.entries)} articles from {rss_feed}.\n")
    else:
        s.speak(f"\nNo articles found in {rss_feed}\n")
    return feed.entries

### Function to get a yes or no answer from the user
def get_yes_no(prompt, default="yes"):
    if DEFAULT_STT_RETRIES == -1:
        print()
        return default
    else:
        s.speak(prompt)
    retiry_no = 0
    answer = ""
    while answer == "":
        user_response = l.listen()
        print(f"You: {user_response}\n")
        if user_response.lower() in ["yes", "sure", "ok", "read it", "yes please", "yup"]:
            answer = "yes"
        elif user_response.lower() in ["no", "nope", "not now", "skip", "no thanks", "no please"]:
            answer = "no"
        elif retiry_no != DEFAULT_STT_RETRIES:
            s.speak("I didn't understand that. Please answer with yes or no.")
            retiry_no += 1
        else:
            answer = default
    return answer

### Function to inform the user how to install Ollama
def how_to_install_ollama():
    dash_line() #------------------------------------------
    s.speak("The easiest way to install ollama is to download the zip-file matching your setup from https://github.com/ollama/ollama/releases. Then you just unzip to your choosen directory and enter the ollama executable path and filename at the top of this script. Done! :)")
    dash_line() #------------------------------------------

### Function to check if Ollama is running
def check_for_ollama():
    try:
        ollama.chat(model='llama3.2', messages=[{"role": "user", "content": "Hello"}])
    except Exception as e:
        return False
    return True

### Function to ask the user if they want to start ollama if it is not running and inform them how to install it if it is not found
def start_ollama():
    dash_line() #------------------------------------------
    if START_OLLAMA or get_yes_no("\nOllama is not running. Do you want to start it?", "yes") == "yes":
        s.speak("Starting Ollama...")
        if os.path.isfile(OLLAMA_PATH):
            subprocess.Popen([OLLAMA_PATH, "serve"]) #), shell=True)
            time.sleep(7)

        if check_for_ollama():
            s.speak("Successfully started Ollama.")
            return
        else:
            s.speak("Could not start Ollama. Please double check your path and installation.\n")
    else:
        s.speak("There is an option, use_ollama, at the top of the script to start it without using ollama.")

    how_to_install_ollama()

    if get_yes_no("\nDo you still want news, without using AI summarization?", "yes") == "yes":
        s.speak("Starting news without AI summarization.\n")
        global use_ollama
        use_ollama = False
    else:
        s.speak("Stopping news script.\n")
        print()
        exit(0) #replace with 1 if you want, 1 makes my debugger stop :D

### Function to check if the playwright mini browser is installed
def check_for_playwright():
    try:
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

### Function to install playwright binaries (<400MB) if it is not installed, first asking the user for permission
def install_playwright():
    dash_line() #------------------------------------------
    if get_yes_no("\nMicrosoft Playwright is not installed. It is used to download articles from sites using anti-scraping. Do you want to install it (<200MB)?", "yes") == "yes":
        s.speak("Installing Playwright...")

        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "--with-deps"], check=True)
        except subprocess.CalledProcessError:
            print("\nPlaywright failed to install with dependencies on this system.")
            print("Playwright is used to download articles from pages with anti-scraping restrictions.")
            print("Manual install instructions: https://playwright.dev/python/docs/intro")
            print("You can also try: python -m playwright install\n")

        if check_for_playwright():
            s.speak("Successfully installed Playwright.")
            return
        else:
            s.speak("Could not install Playwright. Disabling Playwright fallback.\n")
            s.speak("If you are using a virtual python environment you have to install playwright manually outside the environment using: python -m playwright install --with-deps")
            global use_playwright
            use_playwright = False

### Function to check if an article is old or already read, also prints the title and published date if available
def print_info_n_check_if_old_or_read():
    if "title" in entry and "published" not in entry:
        s.speak(f"Title: {entry.title}")
        return False

    if "published" in entry:
        published_date = parser.parse(entry.published) #fix date format
        days =(datetime.now(timezone.utc) - published_date).days #how old is the article
        if days <= DEFAULT_ARTICLE_DAYS: # The article is new enough
            if "title" in entry:
                s.speak(f"Title: {entry.title}")
            s.speak(f"Published: {published_date.strftime('%Y-%m-%d')}")
            return False
        else: #old article - just print the info
            #global old_articles
            #old_articles += 1
            #if old_articles >= GIVE_UP_AFTER_N_OLD:
            #    pass
            #    #TODO! Need to change the functionality of the main loop since this needs to continue two levels
            if "title" in entry:
                print(f"Title: {entry.title}")
            print(f"Published: {published_date.strftime('%Y-%m-%d')}")
            print(f"Article is older than {DEFAULT_ARTICLE_DAYS} days. Skipping.")
            print()
            time.sleep(1)
            return True

### Function to download an article from a given URL
def download_article(url):
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred while downloading the article.")
        return ""
    return response.content #text

### Function to download an article from a given URL, using Playwright to bypass anti-scraping
def download_article_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            #slow_mo=1000,
            #args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1366, "height": 768},
            #locale="en-US",
            #java_script_enabled=True
        )
        page = context.new_page()

        try:
            page.goto(url,
                timeout=60000,
                #wait_until="domcontentloaded"
                wait_until="networkidle",
                #referer="https://www.google.com/"
            )
        except TimeoutError:
            return ""

        html = page.evaluate("""() => {
            // More robust hydration check
            if (typeof window.__REACT_HYDRATED__ !== 'undefined' && !window.__REACT_HYDRATED__) {
                document.dispatchEvent(new CustomEvent('app-ready'));
            }
            return new XMLSerializer().serializeToString(document); // Most comprehensive capture
        }""")

        return html.encode("utf-8")

### Function to get the encoding and string content from a response
def get_format_n_string(content): #
    try:
        return "utf-8", content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return "windows-1252", content.decode('windows-1252')
        except UnicodeDecodeError:
            try:
                return "latin1", content.decode('latin1')
            except UnicodeDecodeError:
                try:
                    return "ISO-8859-1", content.decode('ISO-8859-1')
                except UnicodeDecodeError:
                    try:
                        return "ascii", content.decode('ascii')
                    except UnicodeDecodeError:
                        return "unredable", content

### Function to extract the title and content from a webpage using Readability
def extract_article_from_webpage(html):
    try:
        doc = Document(html)
        title = doc.short_title()
        content = doc.summary()
    except Exception as e:
        print(f"Error: {e}")
        s.speak("An error occurred while extracting the article from the webpage.")
        return "", ""
    return title, content

### Function to convert HTML content to plain text using BeautifulSoup
def convert_html_to_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.text
                    
### Function to generate a summary of an article using Ollama
def generate_article_summary(article_html, lenth):
    summary = ollama.chat(model='llama3.2', messages=[
        {"role": "system", "content": f"Summarize the following article in approximately {lenth} words. Answer only with the summary."},
        {"role": "user", "content": article_html}
    ])
    return summary.message.content

### Function to get the content/summary/description of a feed entry
def get_feed_entry_content(entry):
    if 'content' in entry:
        print(f"entry.content[0].value: {entry.content[0].value}")
        return entry.content[0].value #TODO! Check for more that [0]
    elif 'summary' in entry and entry.summary != entry.title:
        print(f"entry.summary: {entry.summary}")
        return entry.summary
    elif 'description' in entry and entry.description != entry.title:
        print(f"entry.description: {entry.description}")
        return entry.description
    else:
        return None

### Main function to run the script #################################################
if __name__ == "__main__":

    s = speaker.Speaker(also_print=True, speed=DEFAULT_TTS_SPEED)
    l = listener.Listener()

    ollama_process = None

    if use_ollama and not check_for_ollama():
        ollama_process = start_ollama()

    if use_playwright and not check_for_playwright():
        install_playwright()

    s.speak("\nHere are the latest articles from your RSS feeds.")

    for rss_feed in rss_feeds:

        entries = get_feed_entries(rss_feed[3]) #feed_url
        if not entries:
            continue

        #print("This feed has the following keys:")
        #print_key_names(feed)

        for entry in entries:

            dash_line() #------------------------------------------

            skip_article = print_info_n_check_if_old_or_read()
            if skip_article:
                continue

            link_fail = False
            if "link" in entry:
                print(f"Link: {entry.link}")

                if "playwright" not in rss_feed[5]:
                    print("Trying to download article...")
                    article_html = download_article(entry.link)
                elif "playwright" in rss_feed[5] and use_playwright:
                    print("Trying to download article using playwright...")
                    article_html = download_article_playwright(entry.link)
                else:
                    article_html = ""

                if article_html:
                    article_format, article_string = get_format_n_string(article_html)

                    if article_format == "unredable":
                        s.speak("Error decoding response:")
                        print(article_string[:100])
                        article_html = ""
                    else:
                        #print(f"Format: {article_format}")
                        article_html = article_string

                    title, article_html_fixed = extract_article_from_webpage(article_html)
                    article_text = convert_html_to_text(article_html_fixed)
                else:
                    article_text = ""

                word_count = len(article_text.split())
                print(f"Word count: {word_count}")
                average_word_length = len(article_text) / word_count if word_count > 0 else 0

                if word_count == 0:
                    if get_yes_no("The article has zero length. Do you want to open the link in a browser?", "no") == "yes":
                        open_new_tab(entry.link)
                    link_fail = True

                elif article_format == "latin1" and average_word_length > 20: #lower? one had 10 and was binary data
                    if get_yes_no("The article appears to have longer words than normal. This is probably binary data. Do you want to open the link in a browser?", "no") == "yes":
                        open_new_tab(entry.link)
                    #if get_yes_no(f"The average word length is {average_word_length:.2f}. Do you still want me to read this?", "no") == "no":
                    article_text = ""
                    link_fail = True

            else: #"link" not in entry
                s.speak("No link found in entry.")
                article_text = ""
                link_fail = True

            if link_fail:

                # If we didn't get the article text from the link, try to get as much as we can from the feed entry
                text = get_feed_entry_content(entry)
                if text is not None:
                    article_text = convert_html_to_text(text)
                else:
                    article_text = ""
                    if get_yes_no("Can't read the article. Do you want to open the link in a browser?", "no") == "yes":
                        open_new_tab(entry.link)

            if article_text != "":

                # For very short articles, read the article text directly
                if word_count > 0 and word_count < 100:
                    if link_fail:
                        s.speak("Reading summary, content or description:")
                    else:
                        s.speak("Reading article:")
                    s.speak(article_text)

                else:
                    # Read summary
                    if not ALWAYS_READ_LONG:
                        if use_ollama:
                            print("Generating short summary...")
                            s.speak(f"\n{generate_article_summary(article_text, 50)}\n")
                        elif 'summary' in entry and entry.summary != entry.title:
                            print("Reading RSS feed summary:")
                            s.speak(entry.summary)
                        else:
                            print("No summary for this article.")

                    # Read full article
                    if ALWAYS_READ_LONG or get_yes_no("Do you want me to read the article?", "yes") == "yes":

                        if use_ollama and word_count > (DEFAULT_ARTICLE_LENGTH + 100):
                            print(f"Generating summary (approximate length {DEFAULT_ARTICLE_LENGTH})...")
                            summary_long = generate_article_summary(article_text, DEFAULT_ARTICLE_LENGTH)
                            #print(f"Summary word count: {len(summary_long.split())} (Original: {word_count})")
                            s.speak(f"\n{summary_long}\n")
                        else:
                            print("Reading full article:")
                            s.speak(article_text)

            print()
            time.sleep(1)
    
    if ollama_process is not None:
        s.speak("Stopping Ollama.")
        ollama_process.terminate()
        ollama_process.wait()

    s.speak("Finished reading articles.")
    print()
