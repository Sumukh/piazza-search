#Uses Python3 

import json, re, html.parser
from algoliasearch import algoliasearch
import piazza_api as piazza
import config 
import tempfile


# Initialize API Client & Index
client = algoliasearch.Client(config.aloglia_id, config.algolia_key)

search = client.initIndex('CS61A Fa14 Index')

classid = config.classid

p = piazza.PiazzaAPI(classid)
p.user_auth(config.email, config.password)

h = html.parser.HTMLParser()

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    # htmlCodes = (('"', '&#34;'), ('-', '&#43;') ('"', '&amp;#34;'), ('@', '&amp;#64;') , (' ', '&nbsp;'), ("'", '&#39;'),('"', '&quot;'),('"', '&34;'),('>', '&gt;'),('<', '&lt;'),('&', '&amp;'))
    # for code in htmlCodes:
    #     s = s.replace(code[1], code[0])
    return h.unescape(s)

def readTempFile():
	try: 
		info = open('results.txt', 'r')
		data = info.read()
		return int(data)
	except:
		return None

def writeTempFile(endPost):
	try: 
		info = open('results.txt', 'w')
		data = info.write(str(endPost))
	except:
		return None


def process(start=6):
	array = []

	# Count the times we've failed so we know when to stop.
	last_fail_counter = 0

	# i is the post counter
	i = start - 1

	# iterate over results and send them by batch of 10000 elements
	while last_fail_counter < 5:
		i += 1

	    # select the identifier of this row
		post = p.get(i)
		
		# Post is now a dictionary of the post we have. 

		if post['error'] != None or post['result'] == None:
			last_fail_counter += 1
			pass
		else: 
			result = post['result']
			row = {}

			if 'data' in result:
				if 'status' in result:
					if result['status'] == "private":
						pass

			if 'status' in result:
				if result['status'] == "private":
					pass

			last_fail_counter = 0
			row['objectID'] = i


			row['qid'] = i
			row['urlto'] = 'https://piazza.com/class/'+classid+'?cid='+str(i)

			if 'tags' in result:
				row['tags'] = result['tags']

				if 'private' in result['tags']:
					pass

				if 'pin' in result['tags']:
					row['pinned'] = 1
				else:
					row['pinned'] = 0

			if 'history' in result:
				row['postContent'] = html_decode(striphtml(html_decode(result['history'][0]['content'])))
				row['subject'] = html_decode(result['history'][0]['subject'])

	 		#Metrics
			if 'tag_good_arr' in result:
				row['good_q'] = len(result['tag_good_arr'])
			if 'bookmarked' in result:
				row['bookmarked'] = result['bookmarked']
			if 'num_favorites' in result:
				row['num_favorites'] = result['num_favorites']

			if 'is_tag_good' in result:
				if result['is_tag_good']:
					row['is_tag_good'] = 1
				else:
					row['is_tag_good'] = 0

			if 'children' in result: 
				for elem in result['children']:
					if 'subject' in elem:
						if 'followups' in row:
							row['followups'] += html_decode(striphtml(html_decode('\n' + elem['subject'])))
						else:
							row['followups'] = html_decode(striphtml(html_decode(elem['subject'])))
					if 'history' in elem:
						row['responses'] = html_decode(striphtml(html_decode(elem['history'][0]['content'])))

			row['raw_data'] = result
			print(i)

			array.append(row)

			if len(array) == 35:
				search.saveObjects(search)
				array = []
				print("saving to search")

	search.saveObjects(array)

	lastSuccess = i - last_fail_counter

	print("Stopped at "+str(lastSuccess))

	writeTempFile(lastSuccess)

leftOffAt = readTempFile() 
if leftOffAt is None:
	leftOffAt = 6

process(leftOffAt)
