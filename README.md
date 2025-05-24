# BooruLinkPrompt
A StableDiffusion-WebUI Forge script to get a list of tags from supported image boards and add to a prompt.
Currently supported URLs:
- gelbooru.com
- danbooru.donmai.us
- aibooru.online
- rule34.xxx
- chan.sankakucomplex.com[1]
- idol.sankakucomplex.com[1]

[1]: Sankaku Complex requires the user log in to see the entire list of tags. This script currently does not support this functionality. I'd like to add it at a later point, but I don't feel that my Python skills are currently up to the task. I'm going to leave it as a todo item for later at this time. ~TrueKam

## Future Plans
- All planned boorus are currently supported.
- Allow name and password for sites that don't show all the tags for anonymous users. (Looking at you, Sankaku Complex.)
    - To do this, I'll have to figure out how SD-WebUI handles creating settings pages so I don't have to force end users to manually edit this script since some might not have the level of comfort required to do so. It'll take some work, so it's currently back-burnered.

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
- 1.3.1
    - Fixed typo causing Danbooru and AIbooru links containing URL query parameters (usually from site searches) causing errors when trying to fetch.
- 1.4.0
    - Added support for rule34.xxx links.
- 1.5.0
    - Added support for chan.sankakucomplex.com and idol.sankakucomplex.com.