import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime

async def fetch_html(url, page):
    await page.goto(url, timeout=60000)
    await page.wait_for_load_state("networkidle")
    return await page.content()

def gerar_slug(nome):
    import re, unicodedata
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('utf-8')
    nome = re.sub(r'[^\w\s-]', '', nome.lower())
    return re.sub(r'[-\s]+', '-', nome).strip('-_')

async def get_destaques():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        html = await fetch_html("https://animefire.plus/", page)
        soup = BeautifulSoup(html, "html.parser")
        destaques = []
        carousel = soup.find("div", class_="owl-carousel-l_dia")
        if not carousel:
            print("❌ Carrossel não encontrado.")
            await browser.close()
            return []
        for artigo in carousel.select("div.divArticleLancamentos"):
            a = artigo.find("a", class_="item")
            if not a: continue
            nome = a.find("h3", class_="animeTitle").text.strip()
            link = a.get("href", "")
            img = a.find("img")
            thumb = img.get("data-src") or img.get("src") if img else ""
            destaques.append({
                "nome": nome,
                "link": link,
                "thumbnail": thumb,
                "slug": gerar_slug(nome)
            })
        await browser.close()
        return destaques

async def salvar_destaques():
    destaques = await get_destaques()
    os.makedirs("data", exist_ok=True)
    with open("data/destaques-semana.json", "w", encoding="utf-8") as f:
        json.dump(destaques, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(destaques)} destaques salvos.")

if __name__ == "__main__":
    asyncio.run(salvar_destaques())
