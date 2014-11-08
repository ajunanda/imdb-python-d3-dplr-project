import requests
from pattern import web
from BeautifulSoup import BeautifulSoup

# Explicit URL
url = "http://www.imdb.com/search/title?at=0&sort=num_votes&title_type=feature&year=1950,2014"
r = requests.get(url)
print r.url

# Base URL with GET requests wrapped in a dictionary
url = 'http://www.imdb.com/search/title'
params = dict(sort = 'num_votes', at = 0, title_type = 'feature', year = '1950,2014')
r = requests.get(url, params = params)
print r.url

dom = web.Element(r.text)
for movie in dom.by_tag('td.title')[0:10]:
	title = movie.by_tag('a')[0].content
	year = movie.by_tag('span.year_type')[0].content.strip('(').strip(')')
	genres = movie.by_tag('span.genre')[0].by_tag('a')
	genres = [g.content for g in genres]
	runtime = movie.by_tag('span.runtime')[0].content
	# get rating
	rating_list = movie.by_tag('div.rating-list')[0]
	rating_str = rating_list.title
	rating_end_idx = a.rindex('/')
	rating = rating_str[rating_end_idx - 3: rating_end_idx]
	# get votes
	votes_start_index = rating_str.rindex('(')
	votes_end_index = rating_str.rindex(')')
	votes = rating_str[votes_start_index + 1 : votes_end_index]
	votes = int(votes.strip('votes ').replace(',',''))
	# print the results
	print title, year, genres, runtime, rating, votes