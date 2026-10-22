import re
import pymorphy3
import requests
from bs4 import BeautifulSoup

morph = pymorphy3.MorphAnalyzer()

FACTS_DB = [
    # --- ОТРАВЛЕНИЯ ---
    {
        "keywords": ["поганка", "ядовитый гриб", "отравился грибами"],
        "verdict": "☠️ <b>СМЕРТЕЛЬНАЯ ОПАСНОСТЬ!</b>",
        "explanation": "Бледная поганка — самый ядовитый гриб. Даже маленький кусочек вызывает необратимое поражение печени и почек.",
        "actions": "❗ <b>НЕМЕДЛЕННО вызывайте скорую (103)!</b> Промойте желудок и примите активированный уголь.",
        "source": "Минздрав РФ",
        "url": "https://minzdrav.gov.ru"
    },
    {
        "keywords": ["мухомор"],
        "verdict": "☠️ <b>ОПАСНО ДЛЯ ЖИЗНИ!</b>",
        "explanation": "Мухоморы содержат токсины, вызывающие тяжелое отравление и поражение внутренних органов.",
        "actions": "❗ <b>НЕМЕДЛЕННО вызывайте скорую (103)!</b>",
        "source": "Минздрав РФ",
        "url": "https://minzdrav.gov.ru"
    },
    # --- УКУСЫ ---
    {
        "keywords": ["укусила собака", "бешенство"],
        "verdict": "⚠️ <b>РИСК БЕШЕНСТВА</b>",
        "explanation": "Бешенство — смертельное вирусное заболевание, передающееся через слюну при укусе.",
        "actions": "👉 <b>Срочно обратитесь в травмпункт или антирабический кабинет.</b> Врач назначит курс прививок.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/rabies"
    },
    # --- БОЛЕЗНИ ---
    {
        "keywords": ["чума", "бубонная"],
        "verdict": "🦠 <b>ЧУМА</b>",
        "explanation": "Чума — особо опасное инфекционное заболевание. Передается через укусы блох или воздушно-капельным путем.",
        "actions": "✅ <b>Важно:</b> современная чума <b>лечится антибиотиками</b>.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/plague"
    },
    {
        "keywords": ["тиф", "брюшной"],
        "verdict": "⚠️ <b>БРЮШНОЙ ТИФ</b>",
        "explanation": "Брюшной тиф — опасная инфекция. Заразиться можно через грязные руки, воду и еду.",
        "actions": "✅ <b>Важно:</b> тиф лечится антибиотиками. Обратитесь к инфекционисту.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/typhoid"
    },
    {
        "keywords": ["корь"],
        "verdict": "🦠 <b>КОРЬ</b>",
        "explanation": "Корь — высокозаразное вирусное заболевание. Симптомы: температура, кашель, сыпь.",
        "actions": "💊 <b>Что делать:</b> Вызовите врача на дом (болезнь очень заразна!).",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/measles"
    },
    {
        "keywords": ["свинка", "паротит"],
        "verdict": "🦠 <b>СВИНКА (Паротит)</b>",
        "explanation": "Свинка — вирусное заболевание, поражающее слюнные железы.",
        "actions": "💊 <b>Что делать:</b> Постельный режим, обильное питье, вызов врача.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/mumps"
    },
    {
        "keywords": ["туберкулез", "чахотка"],
        "verdict": "🫁 <b>ТУБЕРКУЛЕЗ</b>",
        "explanation": "Туберкулез — инфекционное заболевание, поражающее легкие.",
        "actions": "👉 <b>Срочно обратитесь к врачу-фтизиатру.</b>",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/tuberculosis"
    },
    # --- МИФЫ ---
    {
        "keywords": ["антибиотик", "вирус", "грипп", "простуда", "ковид", "коронавирус"],
        "verdict": "❌ <b>МИФ</b>",
        "explanation": "Антибиотики убивают только бактерии. Они бесполезны против вирусов (ОРВИ, грипп, COVID-19).",
        "actions": "💊 <b>Что делать:</b> При вирусной инфекции антибиотики не помогут.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/antimicrobial-resistance"
    },
    {
        "keywords": ["рак", "воздушно", "заразный", "онкология"],
        "verdict": "❌ <b>МИФ</b>",
        "explanation": "Рак не передается воздушно-капельным путем.",
        "actions": "👉 Для профилактики рака важно вести здоровый образ жизни.",
        "source": "ВОЗ (WHO)",
        "url": "https://www.who.int/ru/news-room/fact-sheets/detail/cancer"
    }
]

PANIC_ROOTS = ["умереть", "смерть", "умирать", "погибнуть", "скончаться", "помереть", "сдохнуть"]

def check_fact(claim: str, last_topic: str = None) -> dict | None:
    clean_claim = re.sub(r'[^\w\s]', ' ', claim.lower()).strip()
    
    if any(root in clean_claim for root in PANIC_ROOTS):
        return {
            "verdict": "🫂 <b>Пожалуйста, не паникуйте.</b>",
            "explanation": "Я — искусственный интеллект и не могу оценить реальную угрозу вашей жизни. Если вам плохо, обратитесь к врачу или позвоните по номеру 103.",
            "source": "Врач / Служба спасения 112",
            "url": "https://minzdrav.gov.ru"
        }

    for fact in FACTS_DB:
        if any(kw in clean_claim for kw in fact["keywords"]):
            return fact
            
    return None

def search_who(query: str) -> dict | None:
    try:
        search_url = f"https://www.who.int/ru/search?query={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        link = soup.find('a', href=re.compile(r'/ru/news-room/fact-sheets/detail/'))
        if link:
            title = link.text.strip()
            url = "https://www.who.int" + link['href']
            return {"title": title, "url": url, "source": "ВОЗ (WHO)"}
    except Exception:
        pass
    return None