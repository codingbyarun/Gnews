import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)

driver.get("https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en")

# Scroll to load more articles
for _ in range(5):
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(3)

# Extract unique news articles
news_data = []
unique_titles = set()  # Store unique titles

articles = driver.find_elements(By.TAG_NAME, "article")

for article in articles:
    try:
        title_element = article.find_element(By.XPATH, ".//a[@target='_blank']")
        title = article.text.strip()
        link = title_element.get_attribute("href")

        # Ensure unique news based on title
        if title and title not in unique_titles:
            unique_titles.add(title)
            news_data.append(f"""
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title"><a href="{link}" target="_blank">{title}</a></h5>
                </div>
            </div>
            """)
    except Exception:
        continue

driver.quit()

# Generate HTML with Bootstrap styling
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Latest News</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">📰 Latest News</a>
        </div>
    </nav>

    <!-- News Section -->
    <div class="container mt-4">
        {"".join(news_data)}
    </div>

</body>
</html>
"""

with open("news.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file 'news.html' created successfully! Duplicate news articles removed.")
