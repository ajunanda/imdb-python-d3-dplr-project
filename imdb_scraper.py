import csv
import re
import requests
from pattern import web

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# CONSTANTS
#######################################################################
NUMBER_MOVIES_BY_VOTES = 228971
NUMBER_MOVIES_PER_PAGE = 50
NUMBER_PAGES_BY_VOTES = NUMBER_MOVIES_BY_VOTES / NUMBER_MOVIES_PER_PAGE
ONE_MILLION = 1000000
K = 1000

# Explicit URL
#######################################################################
url = "http://www.imdb.com/search/title?at=0&sort=num_votes&title_type=feature&year=1950,2014"
url_box_office = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us&title_type=feature&year=1950,2014"
base_url = 'http://www.imdb.com/search/title'

# Helper functions
#######################################################################
def extract_dom(sort, start, url = 'http://www.imdb.com/search/title'):
	params = dict(sort = sort, at = 0, start = start, title_type = 'feature', year = '1950,2014')
	r = requests.get(url, params = params)
	print bcolors.WARNING + r.url + bcolors.ENDC
	return web.Element(r.text)

def extract_title(movie):
	if movie.by_tag('a'):
		return movie.by_tag('a')[0].content.encode('utf').replace(',', '')
	else: return 'NULL'

def extract_year(movie):
	if movie.by_tag('span.year_type'):
		return movie.by_tag('span.year_type')[0].content.strip('(').strip(')')
	else: return 'NULL'

def extract_genres(movie):
	if movie.by_tag('span.genre'):
		genres = movie.by_tag('span.genre')[0].by_tag('a')
		genres = [g.content for g in genres]
		return genres
	else: return ["NULL"]

def extract_runtime(movie):
	if movie.by_tag('span.runtime'):
		runtime = movie.by_tag('span.runtime')[0].content
		runtime = runtime.replace(' mins.', '')
		return int(runtime)
	else: return 'NULL'

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

def extract_box_office_number(movie):
	if movie.by_tag('td.sort_col'):
		box_office_num_str = movie.by_tag('td.sort_col')[0].content
		if 'M' in box_office_num_str:
			box_office_num = float(re.sub('[$M]', '', box_office_num_str)) * ONE_MILLION
		elif 'K' in box_office_num_str:
			box_office_num = float(re.sub('[$K]', '', box_office_num_str)) * K
		elif '-' in box_office_num_str:
			box_office_num = 0
		else: 
			box_office_num = float(re.sub('[$]', '', box_office_num_str))
		return box_office_num
	else: return 'NULL'

def extract_crew_names(movie):
	if movie.by_tag('span.credit'):
		people = movie.by_tag('span.credit')[0].by_tag('a')
		crews = [person.content.encode('utf') for person in people]
		return crews + ['NULL'] * (4 - len(crews))
	else: return ['NULL'] * 4

def extract_certificate(movie):
	if movie.by_tag('span.certificate'):
		elem = movie.by_tag('span.certificate')[0]
		if elem.by_tag('span'):
			return elem.by_tag('span')[0].title
		else: return 'NULL'
	else: return 'NULL'

# Scrape movie data - sorted by num_votes
#######################################################################
f = open('movie_data.csv', 'wb')
writer = csv.writer(f)

try:
	# For some reason, IMDB doesn't return results > 100,000, so I am arbitrarily setting it to 10,000 for now
	for start in range(1, 100 * 100, NUMBER_MOVIES_PER_PAGE):
		print bcolors.WARNING + "Currently processing page number: " + str(start) + "..." + bcolors.ENDC
		dom = extract_dom(sort = 'num_votes', start = start, url = base_url)
		for movie in dom.by_tag('td.title'):
			title = extract_title(movie)
			year = extract_year(movie)
			genres = extract_genres(movie)
			runtime = extract_runtime(movie)
			if movie.by_tag('div.rating-list'):
				rating_list = movie.by_tag('div.rating-list')[0]
				# get rating
				rating = extract_rating(rating_list)
				# get votes
				num_votes = extract_num_votes(rating_list)
			else: rating, num_votes = 0, 0
			# print the results
			print title, year, genres[0], runtime, rating, num_votes
			writer.writerow((title, year, genres[0], runtime, rating, num_votes))
finally:
	f.close()

# Scrape movie data - sorted by box office numbers
#######################################################################
f = open('movie_box_office.csv', 'wb')
writer = csv.writer(f)

try:
	for start in range(1, 100 * 100, NUMBER_MOVIES_PER_PAGE):
		print bcolors.WARNING + "Currently processing box office page number: " + str(start) + "..." + bcolors.ENDC
		dom = extract_dom(sort = 'boxoffice_gross_us', start = start, url = base_url)
		for movie in dom.by_tag('tr.*detailed'):
			box_office_number = extract_box_office_number(movie)
			title = movie.by_tag('a')[0].title[:movie.by_tag('a')[0].title.rfind('(') - 1].encode('utf')
			crews = extract_crew_names(movie)
			certificate = extract_certificate(movie)
			print title, box_office_number, crews[0], crews[1], crews[2], crews[3], certificate
			writer.writerow((title, box_office_number, crews[0], crews[1], crews[2], crews[3], certificate))
finally:
	f.close()
