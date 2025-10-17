# etsy_digital_planner_2026_scraper.py
import time
import re
from datetime import datetime
from urllib.parse import quote_plus
from tqdm import tqdm
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# ========== USER SETTINGS ==========
SEARCH_QUERY = "digital planner 2026"
RESULTS_TO_COLLECT = 300   # number of listings to collect
OUTPUT_CSV = "etsy_digital_planner_2026_raw.csv"
HEADLESS = False           # set True to run without browser window
MAX_PAGES = 50             # max number of search pages to scrape
WAIT_TIME = 2              # seconds to wait between requests

# ========== HELPER FUNCTIONS ==========
def start_driver(headless=HEADLESS):
    options = uc.ChromeOptions()
    if headless:
        options.headless = True
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver

def parse_listing_card(card_soup):
    """
    Extracts basic data from a product card in search results.
    May need selector adjustments if Etsy layout changes.
    """
    a = card_soup.find('a', href=True)
    link = a['href'].split('?')[0] if a else None
    title = a.get_text(strip=True) if a else None

    price = None
    price_span = card_soup.find('span', {'class': re.compile(r'currency-value|price')})
    if price_span:
        price = price_span.get_text(strip=True)

    shop = None
    shop_tag = card_soup.find('div', string=re.compile(r'shop', re.I))

    reviews = None
    review_tag = card_soup.find('span', string=re.compile(r'\d+ reviews|\d+ review', re.I))
    if review_tag:
        reviews = re.findall(r'\d+', review_tag.get_text())
        reviews = int(reviews[0]) if reviews else None

    return {
        "title": title,
        "product_link": link,
        "price_text": price,
        "shop_name": shop,
        "reviews_count": reviews
    }

def extract_from_product_page(driver, product_url):
    """
    Visits each product page to extract more details:
    digital/physical type, image count, category, tags, seller info, total sales, rating.
    """
    result = {
        "is_digital": None,
        "num_images": None,
        "primary_category": None,
        "tags": None,
        "seller_name": None,
        "seller_link": None,
        "total_sales_of_seller": None,
        "rating": None
    }
    try:
        driver.get(product_url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        desc = soup.get_text(" ", strip=True).lower()
        result["is_digital"] = "digital" in desc or "instant download" in desc or "digital download" in desc

        imgs = soup.find_all('img')
        result["num_images"] = len(imgs)

        breadcrumb = soup.find('nav', {'aria-label': 'Breadcrumb'})
        if breadcrumb:
            cats = [c.get_text(strip=True) for c in breadcrumb.find_all('a')]
            result["primary_category"] = cats[-1] if cats else None

        tag_elements = soup.find_all('a', {'data-listing-tag': True})
        if tag_elements:
            result["tags"] = ",".join([t.get_text(strip=True) for t in tag_elements[:10]])
        else:
            result["tags"] = None

        rating_tag = soup.find('span', {'data-rating': True})
        if rating_tag:
            try:
                result["rating"] = float(rating_tag['data-rating'])
            except:
                result["rating"] = None

        seller = soup.find('div', {'data-component-type': 'seller-card'})
        if not seller:
            seller_link_tag = soup.find('a', href=re.compile(r'/shop/'))
            if seller_link_tag:
                result["seller_link"] = "https://www.etsy.com" + seller_link_tag['href'] if seller_link_tag['href'].startswith('/') else seller_link_tag['href']
                result["seller_name"] = seller_link_tag.get_text(strip=True)
        else:
            link = seller.find('a', href=True)
            if link:
                href = link['href']
                result["seller_link"] = href if href.startswith('http') else "https://www.etsy.com" + href
                result["seller_name"] = link.get_text(strip=True)

        if result.get("seller_link"):
            try:
                driver.get(result["seller_link"])
                time.sleep(1)
                seller_soup = BeautifulSoup(driver.page_source, "html.parser")
                sales_text = seller_soup.get_text(" ", strip=True)
                m = re.search(r'(\d[\d,\.]*)\s+sales', sales_text, re.I)
                if m:
                    result["total_sales_of_seller"] = int(m.group(1).replace(',', '').replace('.', ''))
            except Exception:
                result["total_sales_of_seller"] = None

    except Exception as e:
        print("Error extracting product page:", e)
    return result

# ========== MAIN EXECUTION ==========
def main():
    collected = []
    driver = start_driver()
    base_search_url = f"https://www.etsy.com/search?q={quote_plus(SEARCH_QUERY)}"

    try:
        page = 1
        items_collected = 0
        while items_collected < RESULTS_TO_COLLECT and page <= MAX_PAGES:
            url = base_search_url + f"&page={page}"
            print(f"Opening search page: {url}")
            driver.get(url)
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.wt-grid"))
                )
            except:
                time.sleep(2)
            time.sleep(WAIT_TIME)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            cards = soup.select("ul.wt-grid li")
            if not cards:
                cards = soup.select("div.v2-listing-card")

            print(f"Found {len(cards)} listings on page {page}")

            for card in cards:
                if items_collected >= RESULTS_TO_COLLECT:
                    break
                info = parse_listing_card(card)
                if info["product_link"]:
                    full_details = extract_from_product_page(driver, info["product_link"])
                    info.update(full_details)
                    info["collected_at"] = datetime.utcnow().isoformat()
                    collected.append(info)
                    items_collected += 1
                    print(f"Collected: {items_collected} - {info.get('title')}")
                    time.sleep(0.8)
                else:
                    continue

            page += 1
            time.sleep(WAIT_TIME + 1)

        df = pd.DataFrame(collected)
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"\nScraping finished. Saved {len(df)} rows to {OUTPUT_CSV}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
