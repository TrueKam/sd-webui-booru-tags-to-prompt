# Booru Tags to Prompt for Stable Diffusion WebUI Forge
# Script by David R. Collins
#
# Version 1.8.1
# Released under the GNU General Public License Version 3, 29 June 2007
#
# Project based on ideas from danbooru-prompt by EnsignMK (https://github.com/EnsignMK/danbooru-prompt)

# Imports mainly used for SD-WebUI.
import random
import re
import traceback

import gradio as gr
import contextlib

from modules import script_callbacks, scripts, shared
from modules.shared import opts

# Imports primarily for script usage.
import httpx
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen

# Enter your rule34.xxx API key and user ID here. For further information, see:
#   API Info: https://api.rule34.xxx/
#   API Request: https://rule34.xxx/index.php?page=account&s=options
rule34_apiUser = "0000"
rule34_apiKey  = "0000"

scriptUserAgent = "sd-webui-booru-tags-to-prompt/1.8.1"

def on_ui_settings():
    section = ('booru-tags-to-prompt', "Booru Link")

def fetchTags(url):
    """ fetchTags(url)

    This is where the main functionality of the script is kicked off. This function
    takes the URL the user entered and figures out which site it should try to fetch
    tags from before calling the specific function for that site. If the site isn't
    found, it returns an error message into the prompt box.

    Args:
        url (str): The user-provided URL to fetch.

    Returns:
        [string]: A string containing either a comma-separated list of tags found at the provided URL or an error message if the URL is invalid.

    """

    # Figure out which algorithm to use and fetch the necessary tags.
    if "aibooru.online/posts" in url:
        return fetchAibooruTags(url)
    
    elif "danbooru.donmai.us/posts" in url:
        return fetchDanbooruTags(url)
    
    elif "e621.net/posts" in url:
        return fetchESixTwoOneTags(url)
    
    elif "gelbooru.com" in url:
        return fetchGelbooruTags(url)
    
    elif "rule34.paheal.net/post" in url:
        return fetchRuleThirtyFourPahealTags(url)
    
    elif "rule34.xxx" in url:
        return fetchRuleThirtyFourTags(url)
    
    elif "safebooru.org" in url:
        return fetchSafebooruTags(url)
    
    elif ("chan.sankakucomplex.com" in url) and ("posts" in url):
        # This conditional is pretty weird because Sankaku Complex adds "en" between the domain and /posts/.
        # This way /should/ allow any language that they add into the function.
        return fetchSankakuComplexChanTags(url)
    
    elif ("idolcomplex.com" in url) and ("posts" in url):
        # This conditional is pretty weird because Sankaku Complex adds "en" between the domain and /posts/.
        # This way /should/ allow any language that they add into the function.
        return fetchSankakuComplexIdolTags(url)

    elif "tbib.org" in url:
        return fetchTheBigImageBoardTags(url)
    
    else:
        return "Unsupported URL: Must be a post on gelbooru.com, danbooru.donmai.us, chan.sankakucomplex.com, idolcomplex.com, rule34.paheal.net, rule34.xxx, safebooru.org, tbib.org, or aibooru.online"

def fetchAibooruTags(url):
    """ fetchAibooruTags(url)

    Updates the URL to point to AIBooru's JSON post data page instead of the post page
    if necessary. Then get the contents of the post data and parse out the tags to
    return to the frontend.

    Args:
        url (str): The URL on aibooru.online to fetch.

    Returns:
        outputTags: A comma-separated list of formatted tags.

    """

    # Update the URL so it points to the JSON post contents instead of the
    # main page to save just a little bit of bandwidth.
    if "?" in url:
        pos = url.find("?")
        url = url[:pos]
    url = url + ".json"
    
    # Get the contents from the URL and parse it as JSON.
    rawHtml = fetchUrlContents(url)
    parsedHtml = rawHtml.json()

    artistTag = parsedHtml["tag_string_artist"]
    charTag = parsedHtml["tag_string_character"]
    copyrightTag = parsedHtml["tag_string_copyright"]
    metaTags = parsedHtml["tag_string_meta"]
    generalTags = parsedHtml["tag_string_general"]

    # Add the known values of the tags to the list. This is currently broken up because AIBooru makes it easy and doing
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

    return outputTags

def fetchDanbooruTags(url):
    """ fetchDanbooruTags(url)

    Updates the URL to point to Danbooru's JSON post data page instead of the post page
    if necessary. Then get the contents of the post data and parse out the tags to
    return to the frontend.

    Args:
        url (str): The URL on danbooru.donmai.us to fetch.

    Returns:
        outputTags: A comma-separated list of formatted tags.

    """

    # Update the URL so it points to the JSON post contents instead of the
    # main page to save just a little bit of bandwidth.
    if "?" in url:
        pos = url.find("?")
        url = url[:pos]
    url = url + ".json"
    
    # Get the contents from the URL and parse it as JSON.
    rawHtml = fetchUrlContents(url)
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

    return outputTags

def fetchESixTwoOneTags(url):
    """ fetchESixTwoOneTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it.

    Args:
        url (str): The URL on e621.net to fetch.

    Returns:
        tagString: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-list-item"})
    for tag in tagElements:
        thisTag=(unquote(tag['data-name'])).replace("_", " ")
        parsedTags.extend([thisTag])

    tagString = (", ").join(parsedTags).lower()
    return (tagString)

def fetchGelbooruTags(url):
    """ fetchGelbooruTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it.

    Args:
        url (str): The URL on gelbooru.com to fetch.

    Returns:
        imageTags: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

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
    """ fetchRuleThirtyFourTags(url)

    Updates the URL to point to Rule34's JSON post data page instead of the post page
    and add the user's ID and API key, then fetches the data and parses the tag from
    the page.

    Args:
        url (str): The URL on rule34.xxx to fetch.

    Returns:
        parsedTags: A comma-separated list of formatted tags.

    """

    # Convert the URL to the API address and add the user's ID and API key.
    parsedUrl = urlparse(url)
    postId = parse_qs(parsedUrl.query)['id'][0]
    apiUrl = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1&json=1&id=" + postId +"&api_key=" + rule34_apiKey + "&user_id=" + rule34_apiUser

    # Read the post content via the API and parse it as JSON.
    response = fetchUrlContents(apiUrl)
    parsedJson = response.json()

    parsedTags = []
    for tag in parsedJson[0]['tags'].split():
        parsedTags.append(tag)
    parsedTags = (", ").join(parsedTags)

    return parsedTags

def fetchRuleThirtyFourPahealTags(url):
    """ fetchRuleThirtyFourPahealTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it.

    Args:
        url (str): The URL on safebooru.org to fetch.

    Returns:
        parsedTags: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag_name"})
    for tag in tagElements:
        parsedTags.extend(tag.contents)
    tagString = (", ").join(parsedTags).lower()
    
    return tagString

def fetchSafebooruTags(url):
    """ fetchSafebooruTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it.

    Args:
        url (str): The URL on safebooru.org to fetch.

    Returns:
        parsedTags: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

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
    """ fetchSankakuComplexChanTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it. Note
    that currently, the data returned from chan.sankakucomplex.com is generally empty and
    contains no tags to parse.

    Args:
        url (str): The URL on chan.sankakucomplex.com to fetch.

    Returns:
        tagString: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-link"})
    for tag in tagElements:
        parsedTags.extend(tag.contents)
    tagString = (", ").join(parsedTags).lower()
    
    return tagString

def fetchSankakuComplexIdolTags(url):
    """ fetchSankakuComplexIdolTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it. Note
    that currently, the data returned from idolcomplex.com is generally empty and
    contains no tags to parse.

    Args:
        url (str): The URL on idolcomplex.com to fetch.

    Returns:
        tagString: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag-link"})
    for tag in tagElements:
        parsedTags.extend(tag.contents)
    tagString = (", ").join(parsedTags).lower()
    
    return tagString

def fetchTheBigImageBoardTags(url):
    """ fetchTheBigImageBoardTags(url)

    Fetches the HTML contents found at the provided URL and parses the tags from it.

    Args:
        url (str): The URL on tbib.org to fetch.

    Returns:
        tagString: A comma-separated list of formatted tags.

    """

    # Read the HTML content and parse it via BeautifulSoup.
    rawHtml = fetchUrlContents(url)
    parsedHtml = BeautifulSoup(rawHtml.text, 'html.parser')

    parsedTags = []
    tagElements = parsedHtml.find_all(attrs={"class" : "tag"})
    for tag in tagElements:
        parsedTags.extend([tag.find('a').text])
        
    tagString = (", ").join(parsedTags).lower()
    return (tagString)

def fetchUrlContents(url):
    """ fetchUrlContents(url)

    Uses the httpx library to fetch the contents of the URL passed into the
    function and returns the response in raw form. Choice of how to parse that
    response is up to the individual parsing functions due to the different
    supported sites potentially requiring different functionality.

    Args:
        url (str): The pre-parsed and formatted URL to fetch.

    Returns:
        response: An httpx Response containing the data found at the fetched URL.

    """
    # Create the necessary cookies for our session.
    
    cookies = {
        # First one is for e621 to prove we've verified we're over 18.
        'Name':'gw', 'Value':'seen', 'Domain':'e621.net', 'Path':'/', 'HttpOnly':'false', 'Secure':'false', 'SameSite':'Lax'
        # More can be added as necessary. Don't forget a trailing comma on the previous line.
        #'Name':'whatever', 'Value':'nah', etc.
        }
    
    client = httpx.Client(http2=True, headers={'user-agent': scriptUserAgent},follow_redirects=True,cookies=cookies);

    # Read the post content via httpx and save it to 'response.' No error processing
    # is being done here.
    response = client.get(url)

    client.close()

    return response

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
