

files = [
	'allgeyer-v-louisiana.html',
	'hammer-v-dagenhart.html',
	'M\'Culloch v. Maryland.html',
	'marbury-v-madison.html',
	'mugler-v-kansas.html'
]

from bs4 import BeautifulSoup
import re

def pagenum_formatter(soup, file):

	# with open(file) as in_file:
	# 	contents = in_file.read()
	# 	in_file.close()

	# soup = BeautifulSoup(contents, 'html.parser')

	#loop through each <p> that matches the 'Page 100' pattern
	for p in soup.find_all('p',string=re.compile('Page\s\d{1,4}')):

		#extract the page number
		p_split = p.text.split()
		p_num = p_split[1]

		#make a new <span> tag that wraps the page number
		new_span = soup.new_tag("span")
		new_span.string = p_num
		new_span['class'] = 'pagenumber'

		#grab the previous <p> and following <p>
		prev_p = p.find_previous('p')
		next_p = p.find_next('p')

		#look for sentence break patterns and join the sentence fragments, separated by page number <span>
		# if re.search('[^.!?]$', prev_p.text) and re.search('^[a-z]', next_p.text):
		# 	new_p = soup.new_tag('p')
		# 	new_p.append(prev_p.text)
		# 	new_p.append(' ')
		# 	new_p.append(new_span)
		# 	new_p.append(' ')
		# 	new_p.append(next_p.text)
		#
		# 	#throw out the old <p> tags
		# 	prev_p.replace_with(new_p)
		# 	p.replace_with('')
		# 	next_p.replace_with('')

		if re.search('[^.!?]$', prev_p.text) and re.search('^[a-z]', next_p.text):
			prev_p.append(' ')
			prev_p.append(new_span)
			prev_p.append(' ')
			prev_p.append(BeautifulSoup(str(next_p), 'html.parser'))

			#throw out the old <p> tags that held hardcoded Page number
			# prev_p.replace_with(new_p)
			p.replace_with('')
			# next_p.replace_with('')

		#if it doesn't look like a sentence break, then insert page number <span> at beginning of 2nd paragraph, but first inspect anything that passes first test but not second
		else:
			if re.search('[^.!?]$', prev_p.text) and not re.search('^[a-z]', next_p.text):
				print(prev_p)
				print(p)
				print(next_p)
			p.replace_with('')
			next_p.insert(0, new_span)

	#write the new case to file
	filename = file.split('/')[1]
	new_filepath = 'correctedcases/' + filename

	with open(new_filepath, 'w') as out_file:
		out_file.write(str(soup))

	print('EndCase####################\n')

def citation_tagger(file):
	cites = re.compile(
		r'((?:[A-Z][A-Za-z\'-]*(?:\s[A-Z][A-Za-z\'\.-]*)*)\sv\.\s(?:[A-Z][a-z\'-]*(?:\s[A-Za-z][A-Za-z\.\'-]*)*))\,\s((?:[0-9]|[1-9][0-9]|[1-5][0-9][[0-9])\s(?:(?:[A-Z][a-z\.]*(?:\s*[A-Z0-9][a-z\.]*)*))\s(?:[0-9]+))')

	with open(file) as in_file:
		contents = in_file.read()
		in_file.close()

	soup = BeautifulSoup(contents, 'html.parser')

	# replace first match group (casename) with <span> tag wrapping first match group
	total_sub_count = 0
	print('\n')
	print('BeginCase####################\n')
	print(file)
	print('\n')
	for p in soup.find_all('p'):
		if cites.search(p.text):
			matches = cites.findall(p.text)
			for match in matches:
				print(match[0])
				print(match[1])
				print('\n')
			new_p = soup.new_tag('p')
			sub_string, sub_count = cites.subn(
				r'<span class="reference case"><i>\1</i>, <span class="citation">\2</span></span>', p.text)
			new_p_text = BeautifulSoup(sub_string, 'html.parser')
			new_p.append(new_p_text)
			p.replace_with(new_p)
			total_sub_count += sub_count
	print('Substitutions: %d' % total_sub_count)
	return soup, file

# for p in soup.find_all('p'):
# 	if cites.search(p.text):
# 		new_p = soup.new_tag('p')
# 		new_p_text = BeautifulSoup(cites.sub(r'<span class="reference case"><i>\1</i>, <span class="citation">\2</span></span>', p.text), 'html.parser')
# 		new_p.append(new_p_text)
# 		p.replace_with(new_p)

for file in files:
	filepath = 'raw_cases/' + file
	soup_with_citations, source_file = citation_tagger(filepath)
	pagenum_formatter(soup_with_citations, source_file)