import requests
import json
from feedgen.feed import FeedGenerator

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "0.0.0.0"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "" or self.path == '/':
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "ru,en;q=0.9",
                #"Connection": "keep-alive",
                #"Content-Length": "130",
                "Content-Type": "application/json;charset=UTF-8",
                #"Cookie": "_ym_uid=1714112273861660705; _ym_d=1714112273; _ym_isad=2",
                #"Host": "stankin.ru",
                #"Origin": "https://stankin.ru",
                #"Referer": "https://stankin.ru/pages/id_79/news_1",
                #"Sec-Fetch-Dest": "empty",
                #"Sec-Fetch-Mode": "cors",
                #"Sec-Fetch-Site": "same-origin"
            }
            payload = {
                "action":"getNews",
                "data":{
                    "is_main":False,
                    "pull_site":False,
                    "subdivision_id":190,
                    "count":20,
                    "page":1,
                    "tag":"",
                    "query_search":""
                }
            }

            res = requests.post(url="https://stankin.ru/api_entry.php", json=payload, headers=headers)

            fg = FeedGenerator()
            fg.id('http://borislap.ru/stankin_get_news.py')
            fg.title('Аспирантура News')
            #fg.author( {'name':'John Doe','email':'john@example.de'} )
            fg.description("Список новостей аспирантура")
            fg.link( href='http://borislap.ru', rel='alternate' )
            #fg.logo('http://ex.com/logo.jpg')
            #fg.subtitle('This is a cool feed!')
            #fg.link( href='http://larskiesow.de/test.atom', rel='self' )
            fg.language('ru')

            for item in res.json()["data"]["news"]:
                id = item["id"]
                link = f"https://stankin.ru/news/item_{id}"
                fe = fg.add_entry()
                fe.id(link)
                fe.title(item["title"])
                fe.description(item["short_text"])
                fe.link(href=link, rel="alternate")
                fe.pubDate(item["date"])

            rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string

            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            #self.wfile.write(bytes(rssfeed, "utf-8"))
            #self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            #self.wfile.write(bytes("<body>", "utf-8"))
            #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(rssfeed)
            #self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            self.send_error(404, "Not found")

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
