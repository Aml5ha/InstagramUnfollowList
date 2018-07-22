# InstagramUnfollowList
Code for generating a file of people you follow who don't follow you back

This code does not have error checking in case the login information is incorrect. While debugging, I found an issue where the number of followers reflected on the profile does not match the number of actual followers (or following). I verified this by manually counting and found that sometimes an instagram account may actually have +-1 follower/following than the page actually shows. This is accounted for in the code where it checks to see if the number of followers/following found on the page is similar to the number the page shows. 

Like any selenium project, the performance of the program depends on the machine and network. The code may have to be slightly altered to account for slower machines/networks.

The chromedriver used in this project is v 2.4 which supports Chrome v66-68. In the future a more recent version of chromedriver may be needed.

## Overview:
This code works by logging into instagram and navigating to the user's page. The number of followers and following are extracted and stored. The followers button is clicked on and scrolled through until all are loaded and the followers are then parsed and stored in a list. Next, a similar process happens for the following list. Lastly, the two lists are compared and for each person in the following list, if they do not follow you then their instagram handle is printed to a file. 

## Copyright
I made this myself and am fine with anyone improving it or using it. I'd love to hear your thoughts on the project!
