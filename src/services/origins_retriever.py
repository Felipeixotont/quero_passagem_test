import requests
import json
from configs.logger import logger
from configs.vars import USER_AGENT, ACCEPT_LANGUAGE, INDEX_URL

class OriginsRetriever:

    def __init__(self, token: dict):

        self.token = token

    def _request(self):

        self.headers = {
            'User-Agent': USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': ACCEPT_LANGUAGE,
            'Content-Type': 'json',
            'client_id': self.token.get('client_id', None),
            'access_token': self.token.get('access_token', None),
            'x-site-company-id': '7',
            'Origin': INDEX_URL,
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': INDEX_URL + '/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=0',
        }

        api_url = 'https://api.jcatlm.com.br/place/v1/searchOrigin'
        result = dict()

        try:

            response = requests.get(url=api_url, headers=self.headers)

            if response.status_code == 200:
                result = json.loads(response.text)

            else:
                logger.warning(f'{response.status_code} = Verificar Headers.')

        except requests.exceptions.RequestException as e:
            logger.fatal(f'Request failed! Error: {e}')

        finally:
            return result


    def hash_cities(self):

        '''
            Cria uma hash onde: 
            Key == Cidade e Value == ID
        '''

        # conjunto das cidades dos 10 trechos.
        cities_set = {
            'Belo Horizonte',
            'Campinas',
            'Curitiba',
            'Ribeirão Preto',
            'Rio de Janeiro (Novo Rio)',
            'São José do Rio Preto (Rodoviária)',
            'São Paulo (Rod. Tietê)',
            'São Paulo (Rod. Barra Funda)'
        }

        data = self._origins_retriever()
        cities = data.get('result', [])

        response = dict()

        for city in cities:
            if city.get('city') in cities_set:
                response[city.get('city')] = city.get('id')

        return response


    def _origins_retriever(self):
        '''
            Faz a requisição para trazer as origens.
        '''

        data = dict()
        data = self._request()

        return data
