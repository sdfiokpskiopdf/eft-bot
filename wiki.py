from ast import expr_context
import requests
from bs4 import BeautifulSoup


class Wiki:
    def __init__(self):
        self.base_url = "https://escapefromtarkov.fandom.com/wiki/"
        self.b_headings = ["trading", "crafting", "mods", "weapon variants"]

    def lookup(self, term):
        url = self.base_url + term

        data = {}

        for i in range(3):
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content, "lxml")

            exists = soup.find("div", {"class": "noarticletext"})

            if not exists:
                exists = True
                break
            else:
                if i == 0:
                    url = self.base_url + term.upper()
                elif i == 1:
                    url = self.base_url + term.lower()
                else:
                    exists = False
                    data["title"] = term + " Not found"
                    data["url"] = self.base_url + term
                    data["desc"] = "No description found"
                    data[
                        "image"
                    ] = "https://static.thenounproject.com/png/140281-200.png"

        try:
            print(data["title"])
        except:
            print("No title")
        if exists:
            data["title"] = soup.find("h1", {"id": "firstHeading"}).text.strip()
            data["url"] = url

            try:
                image_parent = soup.find("td", {"class": "va-infobox-mainimage-image"})
                data["image"] = image_parent.find("img")["src"]
            except:
                data["image"] = "https://static.thenounproject.com/png/140281-200.png"

            try:
                desc = soup.find("h2", string="Description")
                data["desc"] = desc.find_next_sibling("p").text.strip()
            except:
                data["desc"] = "No description found"
            try:
                heading_parent = desc.parent

                for i in range(2, 10):
                    try:
                        elem = soup.find_all("h2")[i]
                    except IndexError:
                        break

                    if elem.parent == heading_parent:
                        text = elem.text.strip()

                        if text.lower() not in self.b_headings:
                            data[text] = elem.find_next_sibling().text.strip()
                    else:
                        break
            except:
                pass

        return data
