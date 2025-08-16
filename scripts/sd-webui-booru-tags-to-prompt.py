# Booru Tags to Prompt for Stable Diffusion WebUI Forge
# Script by David R. Collins
#
# Version 1.6.1
# Version 1.7.1
# Released under the GNU General Public License Version 3, 29 June 2007
#
# Project based on ideas from danbooru-prompt by EnsignMK (https://github.com/EnsignMK/danbooru-prompt)
import random
import re
import traceback

import gradio as gr
import contextlib

from modules import script_callbacks, scripts, shared
from modules.shared import opts
import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen

def on_ui_settings():
    section = ('booru-tags-to-prompt', "Booru Link")

def fetchTags(url):
    # Figure out which algorithm to use and fetch the necessary tags.
    if "aibooru.online/posts" in url:
        return fetchAibooruTags(url)
    
    elif "danbooru.donmai.us/posts" in url:
        return fetchDanbooruTags(url)
    
    elif "e621.net/posts" in url:
        return fetchESixTwoOneTags(url)
    
    elif "gelbooru.com/index.php" in url:
        return fetchGelbooruTags(url)
    
    elif "rule34.xxx/index.php" in url:
        return fetchRuleThirtyFourTags(url)
    
    elif "safebooru.org/index.php" in url:
        return fetchSafebooruTags(url)
    
    elif ("chan.sankakucomplex.com" in url) and ("posts" in url):
        # This conditional is pretty weird because Sankaku Complex adds "en" between the domain and /posts/.
        # This way /should/ allow any language that they add into the function.
        return fetchSankakuComplexChanTags(url)
    
    elif ("idol.sankakucomplex.com" in url) and ("posts" in url):
        # This conditional is pretty weird because Sankaku Complex adds "en" between the domain and /posts/.
        # This way /should/ allow any language that they add into the function.
        return fetchSankakuComplexIdolTags(url)

    elif "tbib.org/index.php" in url:
        return fetchTheBigImageBoardTags(url)
    
    else:
        return "Unsupported URL; Must be a post on gelbooru.com, danbooru.donmai.us, chan.sankakucomplex.com, idol.sankakucomplex.com, rule34.xxx, safebooru.org, tbib.org, or aibooru.online"

def fetchAibooruTags(url):

    # Get the JSON contents of the post using the passed-in URL.
    if "?" in url:
        pos = url.find("?")
        url = url[:pos]
    url = url + ".json"
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'})
    parsedHtml = rawHtml.json()

    artistTag = parsedHtml["tag_string_artist"]
    charTag = parsedHtml["tag_string_character"]
    copyrightTag = parsedHtml["tag_string_copyright"]
    metaTags = parsedHtml["tag_string_meta"]
    generalTags = parsedHtml["tag_string_general"]

    # Add the known values of the tags to the list. This is currently broken up because Danbooru makes it easy and doing
    # it this way allows optionally removing the artist and character tags later easier. I don't want to implement this
    # until I have a good way to do it for all boorus, though.
    outputTags = ""
    outputTags += artistTag
    outputTags += " " + charTag
    outputTags += " " + copyrightTag
    outputTags += " " + metaTags
    outputTags += " " + generalTags

    # Clean up the tags so they can be dropped into the prompt.
    outputTags = outputTags.replace(" ", ", ")
    outputTags = outputTags.replace("_", " ")
    outputTags = outputTags.replace("(", "\(")
    outputTags = outputTags.replace(")", "\)")
    outputTags = outputTags.replace("[", "\[")
    outputTags = outputTags.replace("]", "\]")
    print(outputTags)
    return outputTags

def fetchDanbooruTags(url):

    # Get the JSON contents of the post using the passed-in URL.
    if "?" in url:
        pos = url.find("?")
        url = url[:pos]
    url = url + ".json"
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'})
    parsedHtml = rawHtml.json()

    artistTag = parsedHtml["tag_string_artist"]
    charTag = parsedHtml["tag_string_character"]
    copyrightTag = parsedHtml["tag_string_copyright"]
    metaTags = parsedHtml["tag_string_meta"]
    generalTags = parsedHtml["tag_string_general"]

    # Add the known values of the tags to the list. This is currently broken up because Danbooru makes it easy and doing
    # it this way allows optionally removing the artist and character tags later easier. I don't want to implement this
    # until I have a good way to do it for all boorus, though.
    outputTags = ""
    outputTags += artistTag
    outputTags += " " + charTag
    outputTags += " " + copyrightTag
    outputTags += " " + metaTags
    outputTags += " " + generalTags

    # Clean up the tags so they can be dropped into the prompt.
    outputTags = outputTags.replace(" ", ", ")
    outputTags = outputTags.replace("_", " ")
    outputTags = outputTags.replace("(", "\(")
    outputTags = outputTags.replace(")", "\)")
    outputTags = outputTags.replace("[", "\[")
    outputTags = outputTags.replace("]", "\]")
    print(outputTags)
    return outputTags

def fetchESixTwoOneTags(url):

    # Create the necessary cookie to prove we've verified we're over 18.
    cookies = { 'Name':'gw', 'Value':'seen', 'Domain':'e621.net', 'Path':'/', 'HttpOnly':'false', 'Secure':'false', 'SameSite':'Lax'}

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.0'}, cookies=cookies).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-list-item"})
    for tag in tagElements:
        thisTag=(unquote(tag['data-name'])).replace("_", " ")
        parsedTags.extend([thisTag])

    tagString = (", ").join(parsedTags).lower()
    return (tagString)

def fetchGelbooruTags(url):

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    # Parse the HTML to find the 'section' element that includes the 'data-md5' attribute, then extract that attribute
    # as the image hash in question.
    imageSection = parsedHtml.body.find('section', {"data-md5": True})
    imageTags = imageSection['data-tags']

    if not imageTags:
        return ("No tags found for the image at that URL.")
    else:
        # Clean up the tag output.
        imageTags = imageTags.strip()
        imageTags = imageTags.replace(" ", ", ")
        imageTags = imageTags.replace("_", " ")
        imageTags = imageTags.replace("(", "\(")
        imageTags = imageTags.replace(")", "\)")
        imageTags = imageTags.replace("[", "\[")
        imageTags = imageTags.replace("]", "\]")
        return (imageTags)

def fetchRuleThirtyFourTags(url):
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    imageElement = parsedHtml.find(attrs={"id" : "image"})

    # imageElement now has the entire <img ... element in it. Get the tags from the "alt" attribute
    # and properly format them.
    parsedTags = []
    for tag in imageElement["alt"].split():
        tag = tag.replace("_", " ")
        parsedTags.append(tag)
    parsedTags = (", ").join(parsedTags)

    return parsedTags

def fetchSafebooruTags(url):
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    imageElement = parsedHtml.find(attrs={"id" : "image"})

    # imageElement now has the entire <img ... element in it. Get the tags from the "alt" attribute
    # and properly format them.
    parsedTags = []
    for tag in imageElement["alt"].split():
        tag = tag.replace("_", " ")
        parsedTags.append(tag)
    parsedTags = (", ").join(parsedTags)

    return parsedTags

def fetchSankakuComplexChanTags(url):
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-link"})
    for tag in tagElements:
        parsedTags.extend(tag.contents)
    tagString = (", ").join(parsedTags).lower()
    
    return tagString

def fetchSankakuComplexIdolTags(url):
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.1'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-link"})
    for tag in tagElements:
        parsedTags.extend(tag.contents)
    tagString = (", ").join(parsedTags).lower()
    
    return tagString

def fetchTheBigImageBoardTags(url):
    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'sd-webui-booru-tags-to-prompt/1.7.0'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag"})
    for tag in tagElements:
        parsedTags.extend([tag.find('a').text])
        
    tagString = (", ").join(parsedTags).lower()
    return (tagString)

class BooruPromptsScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return ("Booru Link to Prompt")

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Booru Link to Prompt", open=False):
                fetch_tags = gr.Button(value='Get Tags', variant='primary')
                link = gr.Textbox(label="Post URL")

            with contextlib.suppress(AttributeError):
                if is_img2img:
                    fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[self.boxxIMG])
                else:
                    fetch_tags.click(fn=fetchTags, inputs=[link], outputs=[self.boxx])

        return [link, fetch_tags]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG = component

script_callbacks.on_ui_settings(on_ui_settings)
