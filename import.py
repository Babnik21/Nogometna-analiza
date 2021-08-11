from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import bs4
import time
import pandas
from os import path
from glob import glob
from dateutil.parser import parse

# Vrne true, če niz predstavlja datum
def is_date(string, fuzzy=False):
    try: 
        parse(string.strip(), fuzzy=fuzzy)
        return True
    except ValueError:
        return False

# Vrne true, če je prvi datum kasnejši kot drugi
def is_recent(date, start_date):
    date = date.split('.')
    start_date = start_date.split('.')
    if int(date[2]) > int(start_date[2]):
        return True
    elif int(date[2]) == int(start_date[2]) and int(date[1]) > int(start_date[1]):
        return True
    elif int(date[2]) == int(start_date[2]) and int(date[1]) == int(start_date[1]):
        return date[0] >= start_date[0]
    else:
        return False

# izračuna razliko dveh datumov
def date_diff(date_1, date_2):
    if date_1 == date_2:
        return 0
    elif is_recent(date_1, date_2):
        first = date_1.split('.')
        second = date_2.split('.')
        diff = 365*(int(first[2]) - int(second[2]))
        diff += 30*(int(first[1]) - int(second[1]))
        return diff + int(first[0]) - int(second[0])
    else:
        return date_diff(date_2, date_1)

# Spremeni procent v delež (50% v 0.5)
def to_rate(percentage):
    return float('0.'+percentage[:-1])

# Vrne ime lige v pravi obliki (brez odvečnih stvari)
def format_league_name(league_text):
    temp = league_text.split('-')
    temp = temp[0].strip()
    temp = temp.split(":")
    return temp[1].strip()

# Odstrani oklepaje (včasih poleg imena ekipe še država izvora, tega ne želimo)
def remove_brackets(word):
    if word[-1] == ")":
        return word[:word.index('(')].strip()
    else:
        return word

# Spremeni tabelo v format, kot ga želimo
def convert_table(list):
    new_list = []
    for el in range(len(list[0])):
        new_sublist = []
        for sl in range(len(list)):
            new_sublist.append(list[sl][el])
        new_list.append(new_sublist)
    return new_list

# Spremeni datum v y-m-d format
def dmy_to_ymd(date):
    date = date.split('.')
    return(date[2]+'-'+date[1]+'-'+date[0])

# Spremeni datum v d.m.y format
def ymd_to_dmy(date):
    date = date.split('-')
    return date[2] + '.' + date[1] + '.' + date[0]

# Zapiše statistiko tekme v csv in vrne True
# Če je tekma že shranjena, vrne False
def stats_to_csv(stat_list, league, season):
    match_id = stat_list[1][0]
    if match_id == "error":
        return None
    elif "Friend" in stat_list[1][1]:
        return None
    file_name = "data/input/{}/{}/{}.csv".format(league, season, stat_list[1][0])  # Sestavi ime datoteke
    frame = pandas.DataFrame.from_records(stat_list[1:], columns=stat_list[0])
    if not path.exists(file_name):
        frame.to_csv(file_name, index=False)
    else:
        return None

# Poišče stran s podatki in vrne seznam s statistiko tekme
def get_match_stats(page, league, team = None, season = None):
    browser = webdriver.Firefox()
    browser.get(page)
    try:
        match_parts = ["Match ", "1st half ", "2nd half ", "Extra time"]
        element = browser.find_elements_by_class_name("statTextGroup")          # Brez tega ne dela (?)
        browser.implicitly_wait(1)
        soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
        tag = soup.find_all('div', {"class": "statTextGroup"})
        imena = soup.find_all('div', {"class": "tname__text"})                  # Poišče imena ekip
        match_time = soup.find_all('div', {"class": "description__time"})       # Poišče datum in čas tekme
        rezultat = soup.find_all('span', {"class": "scoreboard"})               # Poišče rezultat

        match_date = match_time[0].text.strip()[:10]
        teams = [remove_brackets(imena[0].text.strip()), \
            remove_brackets(imena[1].text.strip())]
        match_id = league + "-" + season + '-' + \
            dmy_to_ymd(match_date) + '-' + teams[0] + '-' + teams[1]
        selected_team_index = teams[1] == team 
        season_list = ["season", season]                                        # Za razvrščanje v pravilne stolpce tabele
        medium_list = [["match", match_id], ["league", league]]
        if selected_team_index:
            medium_list += [["home/away", "away"]]
        else:
            medium_list += [["home/away", "home"]]
        medium_list += [["team", teams[selected_team_index]],
            ["opponent", teams[not selected_team_index]],
            ["date", match_date],
            ["goals", rezultat[selected_team_index].text.strip()], 
            ["opponent goals", rezultat[not selected_team_index].text.strip()]]     # Seznam za statistiko (najprej osnovni podatki)
        medium_list.append(season_list)
        counter = -1                                                            # Ugotovi, kateremu delu tekme statistika pripada
        for el in tag:                                                          # Zanka čez vse div-e s statistiko, jo shrani
            stat = []
            mini_list = el.find_all('div')
            for el in mini_list:
                stat.append(el.text)
            if stat[1] == "Ball Possession":                                    #(Ball possession je prva na seznamu), ko jo srečamo je na vrsti statistika iz naslednjega dela tekme
                counter += 1
            medium_list.append([str(match_parts[counter] + stat[1]), \
                stat[2*int(selected_team_index)]])
            medium_list.append([str("opponent " + match_parts[counter] + \
                stat[1]), stat[2*int(not selected_team_index)]])
        browser.quit()
    except:
        browser.quit()
        return [["match", "error"]]
    return medium_list


# Zbere vse tekme iz ene lige in ene sezone, združi v skupno tabelo in shrani v csv
def league_matches_csv(league, season, matches = pandas.DataFrame()):
    filename = "data/input/" + league + '-' + season + '.csv'
    matches_path = glob("data/input/{}/{}/*.csv".format(league, season))
    for csv in matches_path:
        added_frame = pandas.read_csv(csv)
        if added_frame.loc[0, "league"] == remove_brackets(league):
            matches = pandas.concat([matches, added_frame])
    try:
        matches = matches.set_index("match").fillna(0)
    except:
        pass
    matches.to_csv(filename, index=True)
    return matches

# Poišče dno strani (tam je treba klikniti gumb, ki sicer ni viden)
# Poiskal pomoč na Stackoverflow: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
def scroll_down(driver):
    Scroll_pause_time = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(Scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def load_more_matches(browser):
    while True:
        scroll_down(browser)
        # zapre pop-up s piškotki (včasih zamujajo, zato poskusimo ob vsaki ponovitvi)
        try:
            show_matches = browser.find_element_by_css_selector(".event__more")
            show_matches.click()
            time.sleep(3)
        except:
            return browser


# Posodobi celotno sezono za eno ligo
def league_data(league, country, n_teams, season = "2019-2020", n_tries = 0):
    browser = webdriver.Firefox()
    link = "https://www.flashscore.com/football/" + country + \
        "/" + league + "-" + season + "/results/"
    browser.get(link)

    print(link)

    # piškotki
    time.sleep(1)
    try:
        cookies = browser.find_element_by_id("onetrust-accept-btn-handler")
        cookies.click()
        browser.implicitly_wait(2)
    except:
        pass


    browser = load_more_matches(browser)

    game_links = []
    while len(game_links) < n_teams * (n_teams - 1):
        print(len(game_links))
        browser = load_more_matches(browser)
        games = browser.find_elements_by_class_name("event__match")
        game_links = []
        for game in games:
            game_id = game.get_attribute("id")
            game_links.append("https://www.flashscore.com/match/" + \
                game_id[4:] + "/#match-statistics;0")

    print(len(game_links))
    
    browser.quit()              # zapremo browser
    # obišče vsako tekmo in shrani v csv
    for page in game_links:
        statistics = convert_table(get_match_stats(page, league, season = season))
        stats_to_csv(statistics, league, season)

    return None



