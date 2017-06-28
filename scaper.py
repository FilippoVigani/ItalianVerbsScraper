#!/usr/bin/python3

__author__ = "Filipo Vigani"
__copyright__ = "Copyright 2017"
__credits__ = ["Filippo Vigani"]
__license__ = "GNU GENERAL PUBLIC LICENSE"
__version__ = "3.0"
__maintainer__ = "Filippo Vigani"
__email__ = "vigani.filippo@gmail.com"
__status__ = "Beta"

import lxml.html
import requests
import sys
from progress.bar import Bar

QUERY_PREFIX = 'http://www.italian-verbs.com/verbi-italiani/coniugazione.php?parola='
DOMAIN = 'http://www.italian-verbs.com'
BROWSE_VERBS_URL = 'http://www.italian-verbs.com/verbi-italiani/coniugazione.php?browse=A'
LAST_VERB = 'zuzzurellare'
OUPUT_FILE_NAME = 'conjugated_verbs.txt'
BANNED_WORDS = ['Attenzione!', 'ITALIANI;', 'è', '§§§§§'] #words that should not end up in the final file

def scrapeInfinitiveVerbs(url):
	sys.stdout.write("\033[K")
	sys.stdout.write('\r' + 'Scraping verbs list at {}...'.format(url))
	page = requests.get(url)
	tree = lxml.html.fromstring(page.content)
	verbs = tree.xpath("//table/tr/td[@class='browse']/a/text()")
	nextRelativeUrls = tree.xpath("//table/tr/td/a[text()='pagina successiva']/@href")
	nextUrl = DOMAIN + nextRelativeUrls[0] if len(nextRelativeUrls) >= 1 and nextRelativeUrls[0].split('browse=')[-1] != LAST_VERB else None
	return (verbs, nextUrl)

def splitVerbGendersAndQuantify(conjugatedVerb):
	suffixes = conjugatedVerb.split('/') #split on different genders e.g. rischiati/a/e/o
	firstGender = suffixes.pop(0)
	suffixes.append(firstGender[-1])
	unprocessedRoot = firstGender[:-1]
	verbs = []
	if ('(' in unprocessedRoot):
		openSplitted = unprocessedRoot.split('(')
		quantifySplitted = [openSplitted[0]] + openSplitted[-1].split(')') #split on existence quantifier e.h. rim(u)osso -> rimuosso, rimosso
		roots = [quantifySplitted[0] + quantifySplitted[2], unprocessedRoot.replace('(','').replace(')','')]
	else:
		roots = [unprocessedRoot]
	for suffix in suffixes:
		for root in roots:
			verbs.append(root + suffix)
	return set(verbs)

def scrapeVerb(url):
	page = requests.get(url)
	tree = lxml.html.fromstring(page.content)
	conjugatedVerbs = [x for x in map(lambda x: x.replace('—','').strip(), tree.xpath('//table/tr/td/text()')) if x]
	lastWords = set()
	for x in conjugatedVerbs:
		lastWords.update(splitVerbGendersAndQuantify(x.split()[-1]))
	return lastWords

def main():
	#Scraping verbs list
	verbsSet = set()
	currentUrl = BROWSE_VERBS_URL
	while(currentUrl):
		verbs, newUrl = scrapeInfinitiveVerbs(currentUrl)
		verbsSet.update(verbs)
		currentUrl = newUrl

	#Scraping Conjugations
	wordsList = set(verbsSet)
	bar = Bar('Scraping conjugations', max=len(verbsSet))
	while(verbsSet):
		verb = verbsSet.pop()
		currentUrl = QUERY_PREFIX + verb
		wordsList.update(scrapeVerb(currentUrl))

		bar.next()
	bar.finish()

	#Save to file
	bar = Bar('Saving to file %s' % OUPUT_FILE_NAME, max=len(wordsList))
	output = open(OUPUT_FILE_NAME, 'w')
	for item in sorted(wordsList):
		if not (item in BANNED_WORDS) and not ('(' in item):
			output.write("%s\n" % item)
		bar.next()
	output.close()
	bar.finish()
	print("Process completed.")

if __name__ == '__main__':
	main()

