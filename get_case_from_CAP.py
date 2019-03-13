import requests
import json
import pprint


def get_case_id(citation):
	cap_api_url = "https://api.case.law/v1/cases/?cite=" + citation
	r = requests.get(cap_api_url)
	content = r.json()
	cap_case_id = content['results'][0]['id']
	return cap_case_id

def get_case(citation):

	case_id = str(get_case_id(citation))
	cap_api = 'https://api.case.law/v1/cases/'
	headers = {'AUTHORIZATION': 'Token aeb4feab4ea137330201b6e0c8ffaaaa63149bf4'}
	request_url = cap_api + case_id + '?full_case=true'
	r = requests.get(request_url, headers=headers)
	content = r.json()
	short_name = content['name_abbreviation']
	full_name = content['name'].title()
	decisiondate = content['decision_date']
	docketnum = content['docket_number']
	casebody = content['casebody']['data']
	opinion_count = len(content['casebody']['data']['opinions'])
	citations = content['citations']
	citations = json.dumps(citations)
	head_matter = content['casebody']['data']['head_matter']
	opinions = content['casebody']['data']['opinions']
	print('\n')
	print('CAPAPI ID: %s' % case_id)
	print('Short Name: %s' % short_name)
	print('Full Name: %s' % full_name)
	print('Citations: %s' % citations)
	print('Decision date: %s' % decisiondate)
	print('Docket number: %s' % docketnum)
	print('Opinions: %d' % opinion_count)
	print('\n')

	print('HEADMATTER' + '\n')
	print(head_matter)
	print('\n\n\n\n\n')

	opinion_index = 1
	for opinion in opinions:
		print('OPINION' + str(opinion_index))
		print(opinion['type'])
		print(opinion['author'])
		print(opinion['text'])
		print('\n')
		opinion_index += 1

	# print(casebody)

	# filename = name + '.html'
	# filepath = 'raw_cases/' + filename

	# with open(filepath, 'w') as out_file:
	# 	for thing in casebody:
	# 		out_file.write(thing)

# #call function with CAP id as argument
# #TODO loop through a given list of CAP IDs to batch extract the HTML
# get_case(333787)

get_case("561 US 477")

