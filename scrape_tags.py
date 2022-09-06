import pandas as pd
import requests
from bs4 import BeautifulSoup as bsoup
from random import uniform
from numpy import nan
import re

def gen_soup(url):
    current_page = requests.get(url)
    return bsoup(current_page.text, "html.parser")

# DEPRECATED (for now)
def get_dir_writers(soup):
    count = 0
    stuff = []
    for strong_tag in soup.find_all("strong"):
        if count >= 2:
            break
        stuff.append(strong_tag.next_sibling)
    
    # Some field checking. nan if missing.
    if stuff[0]:
        director = stuff[0][1:-1] # [1:-1] because contains a period at the end and first character is a space.
    else:
        director = nan

    if stuff[1]:
        writers = stuff[1].split(", ")
    else:
        writers = nan

    return director, writers

def get_category_and_tags(soup):
    
    # the older pages on the site use the lower version, so we need to account for that.
    try:
        category = soup.find(class_="category").text
        if category.strip() == "Arthouse":
            raise Exception
    except:
        for tag in soup.find(class_="entry-categories"):
            data = [x.text for x in tag.find_all("a")]
            if len(data) == 1:
                category = "Arthouse"
            else:
                category = data[1]

    tags = []
    for tag in soup.find_all(class_="entry-tags"):
        tags.append(tag.text)
    if (not tags) or (len(tags[0].split(" ")) < 2):
        return category.strip(), nan
    return category.strip(), tags[0].split(" ")[1:]

def get_title(soup):
    whole_title = soup.find("title").text
    index_of_rarefilm = whole_title.index("– rarefilmm")
    useless_chars_before = 8
    return(whole_title[:index_of_rarefilm - useless_chars_before])

# regex to get SECOND year in url. first is the year the movie entry 
# was added to the site.
def get_year(url):
    return re.findall(r'.*([1-2][0-9]{3}|3000)', url)[0]
    

# the big one. big piece of shit.
def get_information(url):

    soup = gen_soup(url)

    title = get_title(soup)
    year = get_year(url)
    genre, tags = get_category_and_tags(soup)
    if type(tags) == list:
        country = tags[0]
    else:
        country = nan

    # DEPRECATED. for now.
    # director, writers = get_dir_writers(soup)

    return title, year, genre, country, tags

def generate_dataframe():

    url_df = pd.read_csv("cleaned_urls.csv", index_col=None)
    number_of_entries = url_df.shape[0]

    # title, year, genre, country, director
    main_df = pd.DataFrame(columns = list(["title", "year", "genre", "country"]))

    for i in range(number_of_entries):
        current_url = url_df.url[i] # OK
        current_url_data = [*get_information(current_url)][:4]
        main_df.loc[len(main_df.index)] = current_url_data # OK
        print(f"Entry {i} of {number_of_entries} done.")
        if (i+1) % 100 == 0:
            main_df.to_csv("partial_data.csv", index=False)
            print("partial write done! hundred more.")

    # movie title, year, genre, country, director
    main_df.to_csv("finalised_data.csv", index=False)

if __name__ == "__main__":    

    # ILOC 1199 corresponds to "entry 1201 done.", so 2 off.
    generate_dataframe()