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
                "Content-Type": "application/json;charset=UTF-8",
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

            res = requests.post(url="https://stankin.ru/api_entry.php", json=payload, headers=headers, timeout=10)

            fg = FeedGenerator()
            fg.id('http://borislap.ru/stankin_get_news.py')
            fg.title('Аспирантура News')
            fg.description("Список новостей аспирантура")
            fg.link(href='http://borislap.ru', rel='alternate')
            fg.language('ru')
            
            news = res.json()["data"]["news"]
            for item in reversed(news):
                id = item["id"]
                link = f"https://stankin.ru/news/item_{id}"
                fe = fg.add_entry()
                fe.id(link)
                fe.title(item["title"])
                fe.description(item["short_text"])
                fe.link(href=link, rel="alternate")
                fe.pubDate(item["date"])

            rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string

            fg.lastBuildDate(news[0]["date"])

            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            self.wfile.write(rssfeed)
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
