from bs4 import BeautifulSoup
import re


with open('raw_cases/allgeyer-v-louisiana.html') as in_file:
	contents = in_file.read()
	in_file.close()

case = BeautifulSoup(contents, 'html.parser')

if case('p', string=re.compile('Page\s\d{1,4}')):
	print('yes')
#loop through each <p> that matches the 'Page 100' pattern
# for p in case.find_all('p',string=re.compile('Page\s\d{1,4}')):
#
# 	#extract the page number
# 	p_split = p.text.split()
# 	p_num = p_split[1]
#
# 	#make a new <span> tag that wraps the page number
# 	new_span = case.new_tag("span")
# 	new_span.string = p_num
# 	new_span['class'] = 'pagenumber'
#
# 	#grab the previous <p> and following <p>
# 	prev_p = p.find_previous('p')
# 	next_p = p.find_next('p')
#
# 	#look for sentence break patterns and join the sentence fragments, separated by page number <span>
# 	if re.search('[^.!?]$', prev_p.text) and re.search('^[a-z]', next_p.text):
# 		new_p = case.new_tag('p')
# 		new_p.append(prev_p.text)
# 		new_p.append(' ')
# 		new_p.append(new_span)
# 		new_p.append(' ')
# 		new_p.append(next_p.text)
#
# 		#throw out the old <p> tags
# 		prev_p.replace_with(new_p)
# 		p.replace_with('')
# 		next_p.replace_with('')
#
# 	#if it doesn't look like a sentence break, then insert page number <span> at beginning of 2nd paragraph, but first inspect anything that passes first test but not second
# 	else:
# 		if re.search('[^.!?]$', prev_p.text) and not re.search('^[a-z]', next_p.text):
# 			print(prev_p)
# 			print(p)
# 			print(next_p)
# 		p.replace_with('')
# 		next_p.insert(0, new_span)
#
# #write the new case to file
#
# with open('correctedcases/testing.html', 'w') as out_file:
# 	out_file.write(str(case))


