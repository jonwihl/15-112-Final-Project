from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse

import time

default_states = ["Pennsylvania", "California", "Connecticut"]

def url_generator(states):
    BASEURL = "http://projects.fivethirtyeight.com/election-2016/primary-forecast/"
    parties = ["democratic", "republican"]
    URLSUFFIX = "/#polls-only"

    for s in states:
        for p in parties:
            url = BASEURL + s.lower().replace(" ","-",2) + "-" + p + URLSUFFIX #builds URL based on state and party
            yield {"state": s, "url": url, "party": p}

def parseurl(url):
    candidates = []
    cname = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")


    table = soup.find("table", attrs={"class": "t-polls"})
    # Candidate name
    for c in table.find_all("th", attrs={"class": "th-rotate"}):
        cname.append(str(c.find('span').text))

    # One poll per row
    rows = table.find_all("tr",attrs={"class": "t-row"})
    for idx_cand, c_cand in enumerate(cname): #id_xcand keeps track of the candidate we are building up 
        polldates = []
        pollvalues = []
        candidate = {}
        for row in rows:
            enddate = parse(row['data-end'])
            # handle missing column values
            columns = row.find_all("div", attrs={"class","t-cand-odds"})
            for idx_col, c_col in enumerate(columns):
                if (c_col is None): continue
                if (idx_cand == idx_col):
                    date = enddate.month * 100 + enddate.day
                    if date < int(time.strftime("%m%d")): #only selects 2016 dates
                        polldates.append(enddate.month * 100 + enddate.day)
                        pollvalues.append(float(c_col.text.strip('%'))/100)

        candidate['dates'] = polldates
        candidate['polls'] = pollvalues
        candidate['name'] = c_cand
        candidates.append(candidate)

    return candidates


def scrape(states=default_states):
    data = []
    for u in url_generator(states):
        candidates = parseurl(u['url'])
        for c in candidates:
            tuple = (u['state'], c['dates'], c['polls'], c['name'])
            data.append(tuple)
    return data

def main():
    data = scrape()
    # alternative: data = scrape(["New York", "Massachusetts"])
    for d in data:
        print d

if __name__ == "__main__": #Allows importing of file to TP1.py 
    main()
