
from bs4 import BeautifulSoup
import re
import os

#function to find case citations, wrap them in appropriate tags
def citation_tagger(soup):

	#regex for finding case citations
	cites = re.compile(
		r'((?:[A-Z][A-Za-z\'-]*(?:\s[A-Z][A-Za-z\'\.-]*)*)\sv\.\s(?:[A-Z][a-z\'-]*(?:\s[A-Za-z][A-Za-z\.\'-]*)*))\,\s((?:[0-9]|[1-9][0-9]|[1-5][0-9][[0-9])\s(?:(?:[A-Z][a-z\.]*(?:\s*[A-Z0-9][a-z\.]*)*))\s(?:[0-9]+))')

	#use regex to find citations, wrap citations in new tags, replace old <p> with new <p> 
	for p in soup.find_all('p'):
		if cites.search(p.text):
			new_p = soup.new_tag('p')
			sub_string, sub_count = cites.subn(
				r'<span class="reference case"><i>\1</i>, <span class="citation">\2</span></span>', p.text)
			new_p.append(BeautifulSoup(sub_string, 'html.parser'))
			p.replace_with(new_p)

	return soup

def pagenum_converter(soup):

	#variable to hold anomalous paragraph numbers
	anomalies = []

	# For hardcoded page numbers
	# loop through each <p> that matches the 'Page 100' pattern
	if soup('p', string=re.compile('Page\s\d{1,4}')):

		for p in soup.find_all('p', string=re.compile('Page\s\d{1,4}')):

			# extract the page number
			p_split = p.text.split()
			p_num = p_split[1]

			# make a new <a> tag that wraps the page number
			new_a = soup.new_tag("a")
			new_a.string = '*' + p_num
			new_a['class'] = 'page-number'
			new_a['id'] = 'p' + p_num
			new_a['href'] = '#' + p_num
			new_a['data-citation-index'] = ''

			# grab the previous <p> and following <p>
			prev_p = p.find_previous('p')
			next_p = p.find_next('p')

			# look for sentence break patterns and join the sentence fragments, separated by page number <span>
			if re.search('[^.!?]$', prev_p.text) and re.search('^[a-z]', next_p.text):
				prev_p.append(new_a)
				prev_p.append(' ')
				prev_p.append(BeautifulSoup(str(next_p), 'html.parser'))

				# throw out the old <p> tags
				p.replace_with('')

			# if it doesn't look like a sentence break, then insert page number <span> at beginning of 2nd paragraph, but print anything that passes first test but not second
			else:
				if re.search('[^.!?]$', prev_p.text) and not re.search('^[a-z]', next_p.text):
					anomalies.append(p_num)
				p.replace_with('')
				next_p.insert(0, ' ')
				next_p.insert(0, new_a)

		return soup, anomalies

	# For inline page numbers
	elif soup('p', string=compile('\*\d{1,4}')):

	# regex for finding case citations
		inlinepagenums = re.compile(r'(\*([0-9]|[1-9][0-9]|[1-5][0-9][[0-9]))')

		# use regex to find page numbers and wrap them in <a>tags
		for p in soup.find_all('p'):
			if inlinepagenums.search(p.text):
				new_p = soup.new_tag('p')
				sub_string = inlinepagenums.sub(
					r'<a class="page-number" id="p\2" href="#\2" data-citation-index="1"">\1</a>', p.text)
				new_p.append(BeautifulSoup(sub_string, 'html.parser'))
				p.replace_with(new_p)

		anomalies = 'inline'
		return soup, anomalies

	else:

		anomalies = 'no page numbers'
		return soup, anomalies


def case_cleaner(file):
	new_filename = 'correctedcases/' + os.path.basename(file)

	with open(file) as in_file:
		contents = in_file.read()
		in_file.close()

	soup = BeautifulSoup(contents, 'html.parser')
	soup_with_citations_tagged = citation_tagger(soup)
	soup_with_pagenums_converted, anomalies = pagenum_converter(soup_with_citations_tagged)

	#write the new case to file

	print('\n')
	print(new_filename)
	if anomalies == 'inline' or anomalies == 'no page numbers':
		print("Anomalies: " + anomalies)
	else:
		print("Anomalies: %d" % len(anomalies))
		if len(anomalies) > 0:
			print(anomalies)

	with open(new_filename, 'w') as out_file:
		out_file.write(str(soup_with_pagenums_converted))

directory = '/Users/adam/Dev/cap-play/raw_cases'
for file in os.listdir(directory):
	filepath = os.path.join(directory, file)
	case_cleaner(filepath)
