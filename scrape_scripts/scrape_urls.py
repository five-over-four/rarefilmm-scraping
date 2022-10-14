import pandas as pd
import requests
from bs4 import BeautifulSoup as bsoup
from time import sleep
from random import uniform

def get_previous_link(current_url):

    current_page = requests.get(current_url)
    soup = bsoup(current_page.text, "html.parser")

    # we find all (one) prev classes and within the a href tags.
    prev_class = soup.find_all("p", attrs={"class": "prev"})
    for a_tag in prev_class:
        return(a_tag.find("a")["href"])

def get_all_links(first_url):
    all_urls = [first_url]
    while True:
        previous_link = get_previous_link(all_urls[-1])
        if not previous_link:
            return all_urls
        all_urls.append(get_previous_link(all_urls[-1]))
        sleep(0.1 + uniform(-0.1,0.1))
        print(f"done with {all_urls[-1]}!")

if __name__ == "__main__":
    # starting page only first. traverse through linked list on site.
    first_url = "https://rarefilmm.com/2022/08/utz-1992/"
    all_urls = get_all_links(first_url)
    all_urls_df = pd.DataFrame(all_urls)
    all_urls_df.to_csv("E:/Software/dev/python/data_science_project/urls.csv", index=False)
