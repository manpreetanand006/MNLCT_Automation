from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
browser.maximize_window()
browser.get("https://www.cp24.com/")

def go_to_weather():
    browser.find_element(By.LINK_TEXT, "Weather").click()
    # Step 1: Locate the shadow host element (bmw-weather-search-bar)
    shadow_host = browser.find_element(By.CSS_SELECTOR, "bmw-weather-search-bar")
    # Step 2: Access the shadow root (shadow DOM)
    shadow_root = browser.execute_script('return arguments[0].shadowRoot', shadow_host)
    # Step 3: Locate the input element inside the shadow DOM by its type or class
    search_input = shadow_root.find_element(By.CSS_SELECTOR, "input[type='text']")
    # Interact with the element
    search_input.send_keys("Barrie")
    time.sleep(3)

    # Access the shadow root again to get the <ul> element (unordered List)
    #querySelector is method that returns the first element
    dropdown_ul = WebDriverWait(browser, 10).until(
        lambda d: d.execute_script('return arguments[0].shadowRoot.querySelector(".bmw-cities-dropdown__list")',
                                   shadow_host)
    )

    # Step 4: Locate the first item in the <ul> and click it
    first_item = dropdown_ul.find_element(By.CSS_SELECTOR,
                                          "li.bmw-cities-dropdown__list__item:nth-child(2)")  # The second child, as the first is placeholder
    first_item.click()
    time.sleep(3)
    assert_weather_city_changed()


def assert_weather_city_changed():
    shadow_host = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "bmw-current-conditions"))
    )

    # Access the shadow root
    shadow_root = browser.execute_script("return arguments[0].shadowRoot", shadow_host)

    # Locate the city name div within the shadow root
    city_div = shadow_root.find_element(By.CSS_SELECTOR, ".bmw-current-conditions__city")

    # Get the city name text
    city_name = city_div.text
    assert city_name == "Barrie, ON"


def load_first_article():
    first_article = browser.find_element(By.XPATH, "//article[@class='b-top-table-list-xl'][1]")
    browser.execute_script("window.scrollBy(0,400)")
    actions = ActionChains(browser)
    actions.move_to_element(first_article).click().perform()

    try:
        player_button = browser.find_element(By.XPATH, value="//button[@class='jasper-player-icon-button__button--Wolhi']")
    except:
        player_button = None

    if player_button is None:
        # print("player_button is None")
        browser.execute_script("window.scrollBy(0,100)")
        time.sleep(10)
    else:
        browser.execute_script("window.scrollBy(0,650)")
        player_button.click()
        time.sleep(5)  # To wait for ad complete
        video_tag = browser.find_elements(By.TAG_NAME, "video")[0]
        actions.move_to_element(video_tag).click().perform()  # pause

def main():
    load_first_article()
    browser.back()
    time.sleep(2)
    go_to_weather()
    browser.close()


if __name__ == "__main__":
    main()
