from bs4 import BeautifulSoup


def for_stanford():
    # Open and read the HTML file
    with open("./data/Archive _ Stanford Robotics Seminar.html", "r") as f:
        contents = f.read()

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(contents, "html.parser")

    # Find all the seminar titles
    titles = [title.a.text for title in soup.find_all("td", class_="talk-title")]

    # Find all the seminar abstracts
    abstracts = [
        abstract.p.text
        for abstract in soup.find_all("td", class_="talk-abstract-content")
    ]

    # Combine the titles and abstracts into a list of dictionaries
    seminars = [
        {"title": title, "abstract": abstract}
        for title, abstract in zip(titles, abstracts)
    ]

    for t in titles:
        print(t)


def for_gatech():
    # Open and read the HTML file
    with open("./data/IRIM Seminar Series.html", "r") as f:
        contents = f.read()

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(contents, "html.parser")
    # Find all the seminar titles
    titles = [
        title.text.strip()
        for title in soup.find_all(
            "a", class_="lead item-list-title dont-break-out ng-star-inserted"
        )
    ]
    for t in titles:
        print(t)


def for_cmu():
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Start a new browser session
    driver = webdriver.Chrome()

    # List to hold all seminar titles
    seminar_titles = []

    # URL of the first page
    url = "https://www.ri.cmu.edu/ri-seminar-series/"

    # Loop through all pages
    for i in range(15):
        # Navigate to the page
        driver.get(url)

        # Let the page load
        time.sleep(5)

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find all div elements with class 'epyt-gallery-title'
        titles_divs = soup.find_all("div", class_="epyt-gallery-title")

        # Extract titles text and add to the list
        titles = [div.get_text() for div in titles_divs if ":" in div.get_text()]
        seminar_titles.extend(titles)

        # Find the URL of the next page
        # next_button = driver.find_element(By.CLASS_NAME, "epyt-next")
        # # Try to click the "Next" button to navigate to the next page
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    ((By.XPATH, "//div[@class='epyt-pagebutton epyt-next']"))
                )
            )
            next_button.click()
            time.sleep(5)  # wait for the new page to load
        except Exception as e:
            print(f"Could not locate the next button: {e}")
            break

    # Close the browser session
    driver.quit()

    # Print all seminar titles
    for title in seminar_titles:
        print(title)


for_cmu()
