import os
import sys
import json
import time
import requests
from datetime import date
from .access_token_retriever import AccessTokenRetriever
from utils.functions.generate_pdf import generate_pdf
from utils.functions.generate_csv import generate_csv
from utils.functions.dates import generate_seven_dates
from configs.vars import USER_AGENT, ACCEPT_LANGUAGE, INDEX_URL
from configs.logger import logger


class Trips:
    def __init__(self, routes_list: dict, token: dict):

        self.api_url = 'https://api.jcatlm.com.br/route/v1/getRoutes'
        self.routes = routes_list

        self.token = token
        self.retriever = AccessTokenRetriever()

    def __fetch_token(self):
        '''
            Coleta o access_token e client_id
        '''

        self.token = self.retriever.token_retriever()

    def _request(self, data):

        '''
            :param data: parametro json da requisição.
        '''

        headers = {
            'User-Agent': USER_AGENT,
            'Accept-Language': ACCEPT_LANGUAGE,
            'client_id': self.token.get('client_id', None),
            'access_token': self.token.get('access_token', None),
            'Origin': INDEX_URL,
            'Referer': INDEX_URL + '/',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-site-company-id': '7',
        }

        result = dict()
        time_sleep = 5

        try:

            response = requests.post(url=self.api_url, headers=headers, json=data)

            # Se exceder a quantidade de requisições, adicionar sleeptime até voltar a funcionar.
            while response.status_code == 429:
                logger.warning(f'Error {response.raise_for_status}. Retrying...')
                time.sleep(time_sleep)
                response = requests.post(url=self.api_url, headers=headers, json=data)
                time_sleep = time_sleep + 5

            # Erro de autenticação. Token expirado, coletar o token e fazer outra requisição.
            if response.status_code == 400:

                logger.warning(response.status_code)
                self.__fetch_token()

                headers['client_id'] = self.token.get('client_id', None)
                headers['access_token'] = self.token.get('access_token', None)

                response = requests.post(url=self.api_url, headers=headers, json=data)
                result = json.loads(response.text)

            else:
                result = json.loads(response.text)

        except requests.exceptions.RequestException as e:
            logger.fatal(f'Request failed! Error: {e}')

        finally:
            return result


    def _fetch_trips(self, trips):
        '''
            método para buscar as 7 viagens de um trecho.
            :param route: trecho com o id de origem e id de destino.
        '''

        trip_infos = list()
        route_trips = dict()

        # percorre os 7 dias de viagens
        for trip in trips:

            trip_options = trip.get('result').get('servicesList')
            day = trip.get('result').get('date').split('T')[0]

            title = trip.get('result').get('origin').get('city') +\
            '-' + trip.get('result').get('destination').get('city')

            # percorre as opções de viagens no dia
            for option in trip_options:
                info = {
                        'origin': option.get('originDesc'),
                        'destiny': option.get('destinationDesc'),
                        'trip_class': option.get('class'),
                        'seats_qty': option.get('totalSeats'),
                        'price': option.get('price'),
                        'departure_time': option.get('departureDate').split('T')[-1],
                        'departure_arrival': option.get('arrivalDate').split('T')[-1]
                    }

                trip_infos.append(info)

            # Resetar a trip_infos após salvar os dados no route_trips
            route_trips[day] = trip_infos
            trip_infos = list()

        logger.info('GERANDO PDF...')
        generate_pdf(file_name=title, trips=route_trips)
        generate_csv(file_name=title, trips=route_trips)


    def fetch_routes(self):
        '''
            Percorre os 10 trechos e faz as requisições.
        '''

        trips = list()

        # Loop para iterar sobre os 10 trechos
        for index in range(1, 11):

            # Gerar uma lista com as 7 datas e iterar sobre elas para cada request.
            today = date.today()
            days_list = generate_seven_dates(today)

            origin = self.routes[index].get('origin')
            destination = self.routes[index].get('destination')

            for day in days_list:

                data = {
                    "origin": origin,
                    "destination": destination,
                    "departureDate": day,
                    "availability": True
                }

                response = self._request(data=data)

                if not response:
                    logger.fatal(
                        'Não foi possível concluir a execução do Scraper.'\
                        'Debugar a request no endpoint getRoutes.'
                    )
                    sys.exit(1)

                trips.append(response)

                origin_name = response.get("result").get('origin').get('city')
                destination_name = response.get("result").get('destination').get('city')

                logger.info(f'Coletando dados do trecho {origin_name} x {destination_name} - {day}')

            # Passa a lista com as viagens dos 7 dias para fetch_trips e depois limpa a lista trips
            self._fetch_trips(trips)
            trips = list()
            os.system('clear')
