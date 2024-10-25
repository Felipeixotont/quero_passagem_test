trechos = [
    {'origin': 'São Paulo (Rod. Tietê)', 'destination': 'Belo Horizonte'},
    {'origin': 'Belo Horizonte', 'destination': 'São Paulo (Rod. Tietê)'},
    {'origin': 'São Paulo (Rod. Tietê)', 'destination': 'Ribeirão Preto'},
    {'origin': 'Ribeirão Preto', 'destination': 'São Paulo (Rod. Tietê)'},
    {'origin': 'São Paulo (Rod. Tietê)', 'destination': 'Curitiba'},
    {'origin': 'Rio de Janeiro (Novo Rio)', 'destination': 'Belo Horizonte'},
    {'origin': 'São Paulo (Rod. Barra Funda)', 'destination': 'São José do Rio Preto (Rodoviária)'},
    {'origin': 'Curitiba', 'destination': 'São Paulo (Rod. Tietê)'},
    {'origin': 'São José do Rio Preto (Rodoviária)', 'destination': 'São Paulo (Rod. Barra Funda)'},
    {'origin': 'Rio de Janeiro (Novo Rio)', 'destination': 'Campinas'},
]

def routes(cities):
    '''
        :param cities: hash contendo todas as cidades dos trechos
        com seus ids.
    '''

    i = 1
    data = dict()

    # Organiza o parametro "json" da request para cada trecho a ser pesquisado.
    for trecho in trechos:

        data[i] = {
            'origin': cities.get(trecho.get('origin')),
            'destination': cities.get(trecho.get('destination')),
            'availability': True
        }

        i+=1

    return data
