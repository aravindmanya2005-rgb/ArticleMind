import pandas as pd
import os
import urllib.parse


# ============================================================
# 1. SET PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "train.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "articles_with_urls.csv"
)


# ============================================================
# 2. CHECK WHETHER train.csv EXISTS
# ============================================================

if not os.path.exists(INPUT_FILE):
    print("❌ train.csv was not found.")
    print()
    print("Expected location:")
    print(INPUT_FILE)
    exit()


# ============================================================
# 3. READ train.csv
# ============================================================

print("📂 Reading train.csv...")

df = pd.read_csv(INPUT_FILE)

print(f"✅ Dataset loaded successfully.")
print(f"📊 Total articles found: {len(df)}")


# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
)


# ============================================================
# 5. CHECK FOR TITLE COLUMN
# ============================================================

if "title" not in df.columns:
    print("❌ 'title' column was not found.")
    print("Available columns:")
    print(list(df.columns))
    exit()


# ============================================================
# 6. USE ONLY FIRST 1000 ARTICLES
# ============================================================

df = df.head(1000).copy()

print(f"📰 Using {len(df)} articles.")


# ============================================================
# 7. CREATE ARTICLE SEARCH URL
# ============================================================

def create_article_url(title):

    # Convert title to string
    title = str(title).strip()

    # Encode the title so it can safely be used in a URL
    encoded_title = urllib.parse.quote_plus(title)

    # Create a Google search URL
    url = (
        "https://www.google.com/search?q="
        + encoded_title
    )

    return url


# ============================================================
# 8. CREATE ARTICLE URL COLUMN
# ============================================================

print("🔗 Creating article search links...")

df["article_url"] = df["title"].apply(
    create_article_url
)


# ============================================================
# 9. SAVE NEW CSV FILE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print()
print("============================================")
print("✅ ARTICLE URL FILE CREATED SUCCESSFULLY")
print("============================================")
print()

print("📄 Output file:")
print(OUTPUT_FILE)

print()
print(f"📰 Number of articles: {len(df)}")

print()
print("🔗 Example article links:")
print()

for index, row in df.head(5).iterrows():

    print(f"Article {index + 1}:")
    print(f"Title: {row['title']}")
    print(f"URL: {row['article_url']}")
    print()


print("============================================")
print("🎉 Done!")
print("============================================")