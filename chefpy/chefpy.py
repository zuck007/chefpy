from __future__ import absolute_import, unicode_literals
from bs4 import BeautifulSoup
import sys
import re
import requests
import urllib2
def get_soup(url):
    retry = 2
    html_src = None
    while retry >= 0:
        try:
            html_src = urllib2.urlopen(url).read()
            break
        except Exception as timeout:
            print timeout
            print "......Connecting again......",url
            retry -= 1
    if html_src:
        return BeautifulSoup(html_src,"html.parser")
    else:
        print "Connection Failed"
        sys.exit(1)

    
class Chefpy(object):
    host = "https://www.codechef.com"
    LANG = {"C":[".c","//link: "],
            "C++":[".cpp","//link: "],
            "PYTH":[".py","#link: "],
            "JAVA":[".java","//link: "],
            "C99":[".c","//link: "],
            "C++11":[".cpp","//link: "],
            "C++14":[".cpp","//link: "],
            }

    

    def __init__(self, user):
        self.user = {}
        url = self.host + "/users/" + user
        if requests.get(url, allow_redirects=False).status_code != 200:
            self.status_code = 404
            self.status = 'user not exist'
            return 
        self.status_code = 200    
        soup = get_soup(url)
        self.user["user"] = user
        self.user["rank"] = {}
        self.user["username"] = soup.select("div.user-name-box")[0].text
        stat = soup.select("table .rating-table td hx")

        """
        user["rank"] = {"ContestName":"GlobalRank/CountryRank"}
        """
        self.user["rank"] = {"LongContest":stat[0].text+"/"+stat[1].text,
                                "ShortContest":stat[2].text+"/"+stat[3].text,
                                "LunchTime":stat[4].text+"/"+stat[5].text
                                }
        
        """
        user["problems"] = {"TEST":"https://www.codechef.com/[ContestName]/status/TEST,[USERNAME]",
                                ...
                            }
            
        """
        self.user["problems"] = {}
        for link in soup.select("span a"):
            if self.is_valid(link["href"]):
                problem_code = re.findall(r"/?(\w+)?/status/(\w+),%s"%(self.user["user"]),link["href"])[0][1]
                self.user["problems"][problem_code] = self.host + link["href"]
        
        self.user["status"] = {}
        stat_soup = get_soup(self.host + "/users/" + self.user["user"]).select("table #problem_stats tr td")

        for i in xrange(len(stat_soup)/2):
             self.user["status"][stat_soup[i].text] = stat_soup[9+i].text 



    def is_valid(self, solution_url):
        "check for solution url among all hrefs from user page"
        if re.match(r"/?(\w+)?/status/(\w+),%s"%(self.user["user"]),solution_url):
            return True
        return False
    
    def get_stat(self):
        """
        User:usrename
        ContestName:Global/Country rank
        ...
        ProblemSOlved:..
        ..
        ..
        AC:..
        WA:..
        ..._

        """
        print "Name  : "+self.user["username"]
        print "Contest : Global/Country Rank"
        for contest in sorted(self.user["rank"].keys()):
            print contest +" : "+self.user["rank"][contest]

        for key,val in self.user["status"].iteritems():
            print key + " : " + val


        

    def get_solution(self, problem_code, display=False):
        """Return source code object
        src_code_object = {"format":".c",
                            "text":"#include<std....."
                            }
        """

        if problem_code not in self.user["problems"]:
            print "provide problem code only for those problems which is solved by",self.user
            sys.exit(1)
            
        soup = get_soup(self.user["problems"][problem_code]+"?sort_by=Time&status=15")
        code_lang = soup.select("tr td .centered")[3].text.split(" ")[0]
        code_id = soup.select('tbody tr td')[0].text
        src_code_url = soup.select("tr td ul li a")[0]["href"]
        src_code_url = "http://codechef.com/viewplaintext/" + code_id
        
        #get code from url with indentation & without <pre> tags
        #append problem link as a comment in first line
        src_code_comment = self.LANG[code_lang][1] + self.host+ "/problems/" + problem_code
        src_plain_text = [code.string for code in get_soup(src_code_url).find("pre").children]
        
        if display:
            print src_code_comment + "\n"+ "\n".join(src_plain_text)
        else:
            src_code_object = {"format":self.LANG[code_lang][0],
                           "text": src_code_comment +"\n"+"\n".join(src_plain_text)
                           }
            return src_code_object
