import requests
from pattern import web
from BeautifulSoup import BeautifulSoup

NUMBER_MOVIES_BY_VOTES = 228971
NUMBER_MOVIES_PER_PAGE = 50
NUMBER_PAGES_BY_VOTES = NUMBER_MOVIES_BY_VOTES / NUMBER_MOVIES_PER_PAGE


# Explicit URL
url = "http://www.imdb.com/search/title?at=0&sort=num_votes&title_type=feature&year=1950,2014"
r = requests.get(url)
print r.url

# Base URL with GET requests wrapped in a dictionary
#base_url = 'http://www.imdb.com/search/title'
# params = dict(sort = 'num_votes', at = 0, title_type = 'feature', year = '1950,2014')
# r = requests.get(base_url, params = params)
# print r.url

def extract_dom(start, url = 'http://www.imdb.com/search/title'):
	params = dict(sort = 'num_votes', at = 0, start = start, title_type = 'feature', year = '1950,2014')
	r = requests.get(url, params = params)
	print r.url
	return web.Element(r.text)

def extract_rating(div):
	rating_str = div.title
	end_idx = rating_str.rindex('/')
	return rating_str[end_idx - 3 : end_idx]

def extract_num_votes(div):
	num_votes_str = div.title
	start_idx = num_votes_str.rindex('(')
	end_idx = num_votes_str.rindex(')')
	num_votes = num_votes_str[start_idx + 1 : end_idx]
	return int(num_votes.strip('votes ').replace(',', ''))

# For some reason, IMDB doesn't return results > 100,000, so I am arbitrarily setting it to 50,000 for now
for at in range(1, 50000, NUMBER_MOVIES_PER_PAGE):
	print "Currenting processing page number: " + str(at) + "..."
	dom = extract_dom(at, base_url)

	for movie in dom.by_tag('td.title'):
		title = movie.by_tag('a')[0].content
		year = movie.by_tag('span.year_type')[0].content.strip('(').strip(')')
		genres = movie.by_tag('span.genre')[0].by_tag('a')
		genres = [g.content for g in genres]
		runtime = movie.by_tag('span.runtime')[0].content
		rating_list = movie.by_tag('div.rating-list')[0]
		# get rating
		rating = extract_rating(rating_list)
		# get votes
		num_votes = extract_num_votes(rating_list)
		# print the results
		print title, year, genres, runtime, rating, votes