#!/usr/bin/env python

import urllib
import urllib2

def halte_info(lsn, h, r):
	page = urllib2.urlopen("http://www.connexxion.nl/dashboard/Halteinfo.aspx?lsn=%s&r=%s&h=%s"%(lsn, h, r)).read()
	# Haal alle haltes op van deze pagina's
	page = page[page.find("<table id=\"dienstregeling\""):]
	page = page[:page.find("</table>")]
	haltes = []
	for halte in page.split("</tr>")[1:-1]:
		h = halte[halte.find("&amp;h=")+7:]
		haltes.append(h[:h.find("\"")])
	return haltes



def get_lines(h):
	page = urllib2.urlopen('http://www.connexxion.nl/dashboard/Default.aspx').read()
	start = page.find("<input type=\"hidden\" name=\"__VIEWSTATE\" id=\"__VIEWSTATE\" value=\"") + 64
	end = page.find("\" />", start)
	viewstate = page[start:end]
	start = page.find("<input type=\"hidden\" name=\"__EVENTVALIDATION\" id=\"__EVENTVALIDATION\" value=\"") + 76
	end = page.find("\" />", start)
	eventvalidation = page[start:end]
	eventtarget = "ctl00$mainContent$btnHalte_Zoekhalte"
	page = urllib2.urlopen('http://www.connexxion.nl/dashboard/Default.aspx', urllib.urlencode((
		('__VIEWSTATE', viewstate),
		('__EVENTVALIDATION', eventvalidation),
		('__EVENTTARGET', eventtarget),
		('__EVENTARGUMENT', ''),
		('__VIEWSTATEENCRYPTED', ''),
		('rblHalteZoekop', 'Halte'),
		#('ctl00$mainContent$ddHalte_Reisdatum', '13-1-2011'),
		('ctl00$mainContent$tbHalte_Halte', 'blok'),
		#('ctl00$mainContent$tbLijn_Uur', '01'),
		#('ctl00$mainContent$tbLijn_Minuut', '43'),
		#('ctl00$mainContent$ddLijn_Reisdatum', '13-1-2011'),
	))).read()
	return page



if __name__ == "__main__":
	print get_lines("50320270")


