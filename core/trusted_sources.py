# ==========================================
# БЕЛЫЙ СПИСОК ИСТОЧНИКОВ (Whitelist)
# ==========================================
TRUSTED_DOMAINS = {
    # Уровень 1 — эталонные (100 баллов)
    "uptodate.com": {"weight": 100, "level": 1, "name": "UpToDate"},
    "bestpractice.bmj.com": {"weight": 100, "level": 1, "name": "BMJ Best Practice"},
    "clinicalkey.com": {"weight": 100, "level": 1, "name": "ClinicalKey"},
    "cochranelibrary.com": {"weight": 100, "level": 1, "name": "Cochrane Library"},
    "dynamed.ebscohost.com": {"weight": 100, "level": 1, "name": "DynaMed"},
    "nejm.org": {"weight": 100, "level": 1, "name": "NEJM"},
    "thelancet.com": {"weight": 100, "level": 1, "name": "The Lancet"},
    "bmj.com": {"weight": 100, "level": 1, "name": "BMJ"},
    "pubmed.ncbi.nlm.nih.gov": {"weight": 100, "level": 1, "name": "PubMed"},
    "who.int": {"weight": 100, "level": 1, "name": "ВОЗ (WHO)"},
    "minzdrav.gov.ru": {"weight": 100, "level": 1, "name": "Минздрав РФ"},
    
    # Уровень 2 — авторитетные (70 баллов)
    "medlineplus.gov": {"weight": 70, "level": 2, "name": "MedlinePlus"},
    "msdmanuals.com": {"weight": 70, "level": 2, "name": "MSD Manuals"},
    "mayoclinic.org": {"weight": 70, "level": 2, "name": "Mayo Clinic"},
    "cdc.gov": {"weight": 70, "level": 2, "name": "CDC"},
    
    # Крупные клиники (70 баллов)
    "sechenov.ru": {"weight": 70, "level": 2, "name": "Сеченовский Университет"},
    "medsi.ru": {"weight": 70, "level": 2, "name": "Клиника МЕДСИ"},
    "oncology-centr.ru": {"weight": 70, "level": 2, "name": "Онкоцентр"},
    "nmicr.ru": {"weight": 70, "level": 2, "name": "НМИЦ Радиологии"},
    "nrcii.ru": {"weight": 70, "level": 2, "name": "НМИЦ Инфекционных болезней"},
    
    # Уровень 3 — русскоязычные (60 баллов)
    "mbasegeotar.ru": {"weight": 60, "level": 3, "name": "MedBaseGeotar"},
    "rosmedlib.ru": {"weight": 60, "level": 3, "name": "Консультант Врача"},
    "consilium.orscience.ru": {"weight": 60, "level": 3, "name": "Consilium Medicum"},
    
    # Уровень 4 — дополнительные (50 баллов)
    "medscape.com": {"weight": 50, "level": 4, "name": "Medscape"},
}

def check_domain(url: str) -> dict:
    """Проверяет, есть ли домен в белом списке."""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace("www.", "")
    
    for trusted_domain, info in TRUSTED_DOMAINS.items():
        if domain.endswith(trusted_domain):
            return {
                "trusted": True,
                "weight": info["weight"],
                "level": info["level"],
                "name": info["name"],
            }
    
    return {
        "trusted": False,
        "weight": 0,
        "level": 0,
        "name": "Неизвестный источник",
    }