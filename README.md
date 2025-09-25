# BooruLinkPrompt
A StableDiffusion-WebUI Forge script to get a list of tags from supported image boards and add to a prompt.
Currently supported URLs:
- aibooru.online
- chan.sankakucomplex.com [1]
- danbooru.donmai.us
- e621.net
- gelbooru.com
- idol.sankakucomplex.com [1]
- safebooru.org
- rule34.xxx
- tbib.org

The idea for this script came from danbooru-prompt by EnsignMK (https://github.com/EnsignMK/danbooru-prompt). I wanted to use this functionality but also on other sites, so I coded up the algorithm while lamenting the fact that there isn't a universal API that would get this info. Obligatory XKCD: https://xkcd.com/927/ (The Stable Diffusion taggers work, but not really all that well when compared against a crowd-sourced set of tags.)

[1]: Sankaku Complex requires the user log in to see the entire list of tags. This script currently does not support this functionality. I'd like to add it at a later point, but I don't feel that my Python skills are currently up to the task. I'm going to leave it as a todo item for later at this time. ~TrueKam

## Future Plans
- All planned boorus are currently supported.
- Allow name and password for sites that don't show all the tags for anonymous users. (Looking at you, Sankaku Complex.)
    - To do this, I'll have to figure out how SD-WebUI handles creating settings pages so I don't have to force end users to manually edit this script since some might not have the level of comfort required to do so. It'll take some work, so it's currently back-burnered.

## Version History
Moved to [changelog](/docs/CHANGELOG.md)

## Notes
    1. Sankaku Complex requires the user log in to see the entire list of tags. This script currently does not support this functionality. I'd like to add it at a later point, but I don't feel that my Python skills are currently up to the task. I'm going to leave it as a todo item for later at this time.