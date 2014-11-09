#### Create a local work repo & remote repo on Github

The very first step of setting up a project is to create a local work repository, also known as 'repo' in short. You can do this by simply typing `mkdir myLocalRepo` in the command line. In case your local machine has a failure, you can backup all your work in a remote work repository, hosted on a third party site like Github.com. Remember that github is free so all of your repos will be public and not proprietary.

Creating a remote repo on github is easy, follow the instructions [here](https://help.github.com/articles/create-a-repo/). Once the remote directory is set up, you can simply `git remote add origin https://github.com/robert8138/imdb_project.git` in your local work repo, this effectively will link your local working directory to the remote working directory. Anything that you add, modify on the local directory can be `push` to the remote repo by `git push`.

#### Setting up virtualenv

In my particular case, I knew I am going to write a scraper in Python, so upon setting up my local work directory, I didn't just use `mkdir`. Instead, I created a virtualenv directory by typing `virtualenv imdb_project`. The advantage of virtualenv is that pip is installed by default, so you can install all the python packages using `pip install`. Furthermore, it create a virtual environment where all the package management business is taken care of, so you don't need to worry about namespace collision.

To activate the virtualenv environment, type `source /bin/activate`. Now you are free to pip install your favorite packages

#### Writing a Python scraper

To get started, I model after the scraping exercise in [lab 4] of Harvard CS 109's data science class. The immediate first thing I did before writin a single line of python code is `pip install {requests, pattern, BeautifulSoup}`. 

I basically copied exactly what the lab did, and the result is in scraper.py. The high level idea is simple:

* You use request to send a HTTP GET request. In return, we received a HTML object
* We then use the `pattern.web` to parse out the DOM
* Once we have the DOM, we can traverse through the DOM to find the information we want
	* You can search specific DOM elements by `.by_tag'
	* If interested in the attribute value, simply use `element.attributeName` to see what's in there. 
	* Use `element.HTML` or `element.content` to see the values.

I got the scraper working for the first page, which are only 50 records. If order to store all the data, I will need to loop through and change the start parameter in the url.

###### More resources for scraping using Python

* [Web scraping 101 with Python]
* [More web scraping with Python]
* [Y combinator's response and comparison on scraping packages]
* Libraries:
	* [Requests]
	* [Mechanize]
	* [lxml]

[lab 4]:http://nbviewer.ipython.org/github/cs109/content/blob/master/lec_04_scraping.ipynb
[lab 4 munging]: http://nbviewer.ipython.org/github/cs109/content/blob/master/lec_04_wrangling.ipynb
[Executing python script in sublime]: http://stackoverflow.com/questions/8551735/how-do-i-run-python-code-from-sublime-text-2
[Greg Reda]: http://www.gregreda.com/
[Web scraping 101 with Python]: http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/
[More web scraping with Python]: http://www.gregreda.com/2013/05/06/more-web-scraping-with-python/
[Y combinator's response and comparison on scraping packages]: https://news.ycombinator.com/item?id=5353347
[Requests]: http://docs.python-requests.org/en/latest/
[Mechanize]: http://wwwsearch.sourceforge.net/mechanize/
[lxml]: http://lxml.de/
