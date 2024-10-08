from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from database.database_utils import insert_game
from scrapers.gameplay_scraper import get_gameplay_links


def scrape_xbox_games():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.xbox.com/en-us/xbox-game-pass?xr=shellnav")
    time.sleep(5)

    game_info_list = []

    try:
        # Locate the ul element containing the list items
        game_list = driver.find_elements(By.XPATH,
                                         '/html/body/div[1]/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div/div/div/ul/li[position() >= 3 and position() <= 8]')

        for game_item in game_list:
            try:
                game_name_element = game_item.find_element(By.XPATH, './/a')
                game_name = game_name_element.get_attribute('aria-label').split('.')[
                    0]  # Take the part before the first period

                game_link = game_name_element.get_attribute('href')

                try:
                    image_element = game_item.find_element(By.XPATH, './/img')
                    image_src = image_element.get_attribute('src')
                except NoSuchElementException:
                    image_src = None

                game_info_list.append({
                    "name": game_name,
                    "link": game_link,
                    "image_src": image_src
                })
            except NoSuchElementException as e:
                print(f"Error finding element: {e}")

    except NoSuchElementException as e:
        print(f"An error occurred while finding game list: {e}")

    driver.quit()

    game_info_list_with_links = get_gameplay_links(game_info_list)

    # Insert games into the database
    for game_info in game_info_list_with_links:
        insert_game('xbox', game_info)

    return game_info_list


