from django.shortcuts import render

from googleapiclient.discovery import build

from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
import datetime


my_api_key = "AIzaSyDWoW06UEOvs012lZM7-1SWrOow-2f7yr4"
my_cse_id = "005819025646842418275:zlurprlbaaa"



def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def home(request):
	ip = request.META.get('REMOTE_ADDR')
	date = datetime.datetime.now()
	file = open("logs.txt",'a')
	file.write(str(date)+"\n")
	file.close()
	return render(request,'home.html')

def logs(request):
	file = open("logs.txt",'r')
	data = file.read().replace("\n","<br>")
	file.close()
	return HttpResponse(data)

def getData(request):
	start = request.GET.get("start")
	word = request.GET.get("word")
	country = request.GET.get("country")
	print start, word, country

	results = google_search(word, my_api_key, my_cse_id, num=10, start=start,cr=country)
	st = int(start)
	for result in results:
		result["id"] = st
		st = st + 1;
	x =  render(request,"data.html",{"results":results,"start":start,"country":country,"word":word})	
	print x
	return x

def getText(request):
	try:
		link = request.GET.get("link")
		if(link[-4:]) != "pdf":
			response = requests.get(link)
			content = response.content
			soup = BeautifulSoup(content,"lxml")
			for script in soup(["script", "style","head","title"]):
				script.extract()
			cleantext = soup.get_text()
		else:
			cleantext = ""
		print link
		return HttpResponse(cleantext)
	except:
		return HttpResponse("No data. Please click on the link")