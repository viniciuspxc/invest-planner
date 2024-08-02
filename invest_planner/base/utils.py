import requests
from django.core.cache import cache


def get_central_bank_rate():
    # URLs das taxas
    url_cdi = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json"
    url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"

    # Função para obter a taxa do Banco Central
    def fetch_rate(url, cache_key_rate, cache_key_date):
        rate, date = None, None
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                rate = data[-1]['valor']
                date = data[-1]['data']
                # Cache por 1 dia
                cache.set(cache_key_rate, rate, timeout=86400)
                cache.set(cache_key_date, date, timeout=86400)
        return rate, date

    # Obter as taxas e datas do cache ou da API
    cdi_rate, cdi_date = cache.get('cdi_rate'), cache.get('cdi_date')
    if cdi_rate is None or cdi_date is None:
        cdi_rate, cdi_date = fetch_rate(url_cdi, 'cdi_rate', 'cdi_date')

    selic_rate, selic_date = cache.get('selic_rate'), cache.get('selic_date')
    if selic_rate is None or selic_date is None:
        selic_rate, selic_date = fetch_rate(
            url_selic, 'selic_rate', 'selic_date')

    context = {
        'taxes': [
            {'name': 'cdi', 'rate': cdi_rate, 'date': cdi_date},
            {'name': 'selic', 'rate': selic_rate, 'date': selic_date}
        ]
    }
    return context
