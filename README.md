piazza-search
=============

Better search for Piazza (an educational question &amp; answer platform) - Powered by Algolia. 


This uses the Piazza API to get posts and puts them into a searchable format. 

Usage
--------
Create a config.py file with the appropriate details/credentials

then run `python3 search.py` to start gathering the posts. 

It will batch upload to a cloud search provider - Algolia. You can then tweak the index/search settings on Algolia to your liking. 

Then just use the search.html file (with your API keys in the file) to search. 

