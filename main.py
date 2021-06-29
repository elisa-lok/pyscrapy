# encoding=utf-8
import re
import time
import html2text
import requests
from bs4 import BeautifulSoup
import threading
 
def ascii_to_str(text) -> str:
    obj = re.compile(r"&#x(?P<asc>.*?);", re.S)
    ret = obj.finditer(resp.text)
    new_text = resp.text
    for i in ret:
        as_code = i.group("asc")
        find_sr = r"&#x" + as_code + r";"
        string_int = int(as_code, 16)
        new_text = new_text.replace(find_sr, chr(string_int))
    return new_text
 
 
def html_to_md(text, filename) -> None:
    with open(filename, 'w', encoding="utf-8") as file:
        h = html2text.HTML2Text()
        content = h.handle(text)
        file.write(content)
 
def one_page_deal(url_name, header, file_name) -> None:
    resp1 = requests.get(url_name, headers=header)
    bs = BeautifulSoup(resp1.text, "html.parser")
  
    ret1 = bs.find_all("ul", attrs={"class": "summary"})
    for i_index in ret1:
        i_index.decompose()
  
    ret2 = bs.find_all("div", attrs={"class": "search-results"})
    for j in ret2:
        j.decompose()
    html_to_md(str(bs), file_name)
 
 
url = "https://taizilongxu.gitbooks.io/stackoverflow-about-python/content/"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 "
                  "Safari/537.36 Edg/122.0.0.0"
 
}
 
resp = requests.get(url, headers=header)

page = BeautifulSoup(resp.text, "html.parser")
title_name = page.find("title")
file_name = title_name.text.replace(" ", "_") + ".md"
new_string = ascii_to_str(resp.text)
html_to_md(new_string, file_name)

chapter = []
ret = page.find_all("li", attrs={"class": "chapter"})
index = 0
for i in ret:
    if index == 0:
        index += 1
        continue
    url_name = url + i.get("data-path")
    chapter.append(url_name)

threads = []
for i in chapter:
    file_name = str(index) + ".md"
    t = threading.Thread(target=one_page_deal, args=(i, header, file_name))
    t.start()
    threads.append(t)
    index += 1
    time.sleep(1)
 
for i in threads:
    i.join()