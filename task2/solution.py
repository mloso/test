from __future__ import annotations

import asyncio
import csv
import re
from collections import defaultdict

import aiohttp
from bs4 import BeautifulSoup


async def process_page(session, url, letter_counts) -> str | None:
    async with session.get(url) as response:
        html = await response.text()
    soup = BeautifulSoup(html, "html.parser")

    for group in soup.find_all("div", class_="mw-category-group"):
        letter = group.find("h3").text.strip()
        if not re.match(r"^[А-ЯЁ]$", letter):
            continue

        items = group.find_all("li")
        russian_items = [
            item for item in items if re.match(r"^[А-ЯЁа-яё]", item.text.strip())
        ]
        letter_counts[letter] += len(russian_items)

    next_page = soup.find("a", text="Следующая страница")
    return next_page["href"] if next_page else None


async def get_animals_count() -> defaultdict[str, int]:
    base_url = "https://ru.wikipedia.org"
    start_url = base_url + "/wiki/Категория:Животные_по_алфавиту"

    letter_counts = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        current_url = start_url
        while current_url:
            next_page_part = await process_page(session, current_url, letter_counts)
            current_url = base_url + next_page_part if next_page_part else None

    return letter_counts


def save_to_csv(counts, filename="beasts.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        for letter in sorted(counts.keys(), key=lambda x: russian_alphabet.index(x)):
            writer.writerow([letter, counts[letter]])


async def main() -> None:
    save_to_csv(counts=await get_animals_count())


if __name__ == "__main__":
    asyncio.run(main())
