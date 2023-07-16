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


for_gatech()
