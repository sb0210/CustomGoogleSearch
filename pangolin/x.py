from django.shortcuts import render

from googleapiclient.discovery import build

from bs4 import BeautifulSoup
import requests

my_api_key = "AIzaSyDWoW06UEOvs012lZM7-1SWrOow-2f7yr4"
my_cse_id = "005819025646842418275:hlyos5dt7us"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def home(request):
	return render(request,'home.html')


def getData(start,word,country):
	start = request.GET.get("start")
	word = request.GET.get("word")
	country = request.GET.get("country")
	print start, word, country
	results = [{
		"link":"http://google.com"
	}]
	results = google_search(word, my_api_key, my_cse_id, num=10, start=start,cr=country)
	for result in results:
		link = result["link"]
		if(link[-4:]) != "pdf":
			response = requests.get(link)
			content = response.content
			soup = BeautifulSoup(content,"lxml")
			for script in soup(["script", "style"]):
				script.extract()
			cleantext = soup.get_text()
		else:
			cleantext = ""
		result["cleantext"] = cleantext
	return results
	x =  render(request,"data.html",{"results":results,"start":start,"country":country,"word":word})	
	print x
	return x

	