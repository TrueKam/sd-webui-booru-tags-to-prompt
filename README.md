# BooruLinkPrompt
A StableDiffusion-WebUI Forge script to get a list of tags from supported image boards and add to a prompt.
Currently supported URLs:
- gelbooru.com
- danbooru.donmai.us
- aibooru.online

## Future Plans
- Add support for other boorus. Currently planned supported URLs are: ~~danbooru.donmai.us~~, chan.sankakucomplex.com, idol.sankakucomplex.com, and ~~aibooru.online~~

## Version History
- 1.0.0
    - Initial commit. Code functions perfectly well, but only supports gelbooru.com.
- 1.1.0
    - Refactored functionality when button is pressed to parse the URL passed in before attempting to fetch. It still only supports gelbooru.com URLs, but the framework is now in place to allow the rest to be written.
- 1.1.5
    - Refactored to remove redundant URL check and updated gelbooru fetch user agent.
- 1.2.0
    - Danbooru links are now supported.
- 1.3.0
    - AIbooru links are now supported.
