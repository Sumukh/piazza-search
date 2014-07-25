#Uses Python3 

import json, re, html.parser
from algoliasearch import algoliasearch
import piazza_api as piazza
import config 


# Initialize API Client & Index
client = algoliasearch.Client(config.aloglia_id, config.algolia_key)

search = client.initIndex('CS61A Index')

classid = config.classid

p = piazza.PiazzaAPI(classid)
p.user_auth()

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


def process(start=6, end=1500):
	array = []

	# iterate over results and send them by batch of 10000 elements
	for i in range(start,end):
	    # select the identifier of this row
		post = p.get(i)
		
		# Post is now a dictionary of the post we have. 

		if post['error'] != None or post['result'] == None:
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

process()
