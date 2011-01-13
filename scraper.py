#!/usr/bin/env python

import urllib
import urllib2

def get_aspx_fields(page):
	fields = {}
	start = page.find("<input type=\"hidden\" name=\"__VIEWSTATE\" id=\"__VIEWSTATE\" value=\"") + 64
	end = page.find("\" />", start)
	fields["__VIEWSTATE"] = page[start:end]
	start = page.find("<input type=\"hidden\" name=\"__EVENTVALIDATION\" id=\"__EVENTVALIDATION\" value=\"") + 76
	end = page.find("\" />", start)
	fields["__EVENTVALIDATION"] = page[start:end]
	return fields

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
	fields = get_aspx_fields(page)
	eventtarget = "ctl00$mainContent$btnHalte_Zoekhalte"
	page = urllib2.urlopen('http://www.connexxion.nl/dashboard/Default.aspx', urllib.urlencode((
		('__VIEWSTATE', fields["__VIEWSTATE"]),
		('__EVENTVALIDATION', fields["__EVENTVALIDATION"]),
		('__EVENTTARGET', eventtarget),
		('__EVENTARGUMENT', ''),
		('__VIEWSTATEENCRYPTED', ''),
		('rblHalteZoekop', 'Halte'),
		('ctl00$mainContent$tbHalte_Halte', 'blok'),
	))).read()
	fields = get_aspx_fields(page)
	page = urllib2.urlopen("http://www.connexxion.nl/dashboard/Halteinfo.aspx", urllib.urlencode((
		('__VIEWSTATE', fields["__VIEWSTATE"]),
		('__EVENTVALIDATION', fields["__EVENTVALIDATION"]),
		('__EVENTTARGET', 'ctl00$mainContent$btnToonLijnlijst'),
		('__EVENTARGUMENT', ''),
		('__VIEWSTATEENCRYPTED', ''),
		('ctl00$mainContent$ddHaltes', h),
	))).read()
	start_select = page.find('name="ctl00$mainContent$lbLijnen"')
	end_select = page.find('</select>', start_select)
	options = page[start_select:end_select]
	lines = {}
	print options
	while True:
		start = options.find("value=\"") + 7
		if start == 6: break # -1 + 7 == 6
		end = options.find("\">", start)
		id = options[start:end]
		start = options.find(">", end) + 1
		end = options.find("</option>", start)
		name = options[start:end]
		lines[id] = name
		options = options[end:]

	return lines



if __name__ == "__main__":
	print get_lines("37323930")


