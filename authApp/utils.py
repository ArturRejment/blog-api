def StripAndCapital(text):
	name = ''
	text = text.split(" ")
	for word in text:
		word = word.capitalize()
		word = word.strip()
		if len(word) >= 1:
			name += word + ' '
	name = name.strip()
	return name