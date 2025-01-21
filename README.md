# how to use:

- navigate to desired directory, then run

## python site_recursion_scraper.py "https://example.com" depth

where the url is the site you want to scrape and depth is the maximum depth of the json tree

the result of running the script is that in the directory you ran the script in will appear a file called 

# scraped_links.json

any subsequent calls will overwrite the json file with your new links. if you want this to behave differently then just change the code lol

You can also just open up a python file and go

# from site_recursion_scraper import scrape_links

and use it that way