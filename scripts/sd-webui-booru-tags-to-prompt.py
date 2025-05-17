# Booru Tags to Prompt for Stable Diffusion WebUI Forge
# Script by David R. Collins
#
# Version 1.0.0
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
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen

def on_ui_settings():
    section = ('booru-tags-to-prompt', "Booru Link")

def fetchGelbooruTags(url):

    # First, verify that the passed URL is valid.
    if "gelbooru.com/index.php" not in url:
        return "Unsupported URL; Must be a post on gelbooru.com."

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = requests.get(url, headers={'user-agent': 'stable-diffusion-webui-booru-tags-to-prompt/1.0.0'}).text
    parsedHtml = BeautifulSoup(rawHtml, 'html.parser')

    # Parse the HTML to find the 'section' element that includes the 'data-md5' attribute, then extract that attribute
    # as the image hash in question.
    imageSection = parsedHtml.body.find('section', {"data-md5": True})
    imageHash = imageSection['data-md5']

    # Now that the image hash is found, use that to get the post's JSON.
    gelbooruUrl = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=md5:" + imageHash

    # Original code from sd-webui-gelbooru-prompt project follows.
    req = requests.get(gelbooruUrl)
    data = req.json()
    
    if data["@attributes"]["count"] > 1:
        return ("No image found with that hash.")
    else:
        post = data["post"][0]
        tags = post["tags"]

        parsed = []
        for tag in tags.split():
            tag = tag.replace("_", " ")
            parsed.append(tag)
        parsed = (", ").join(parsed)
        return (parsed)

class BooruPromptsScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return ("Booru Link")

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group():
            with gr.Accordion("Booru Link", open=False):
                fetch_tags = gr.Button(value='Get Tags', variant='primary')
                link = gr.Textbox(label="Post URL")

            with contextlib.suppress(AttributeError):
                if is_img2img:
                    fetch_tags.click(fn=fetchGelbooruTags, inputs=[link], outputs=[self.boxxIMG])
                else:
                    fetch_tags.click(fn=fetchGelbooruTags, inputs=[link], outputs=[self.boxx])

        return [link, fetch_tags]

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":
            self.boxx = component
        if kwargs.get("elem_id") == "img2img_prompt":
            self.boxxIMG = component

script_callbacks.on_ui_settings(on_ui_settings)
