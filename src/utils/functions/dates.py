from datetime import timedelta

def generate_seven_dates(first_day, dias=7):
    '''
        :param first_day: Dia atual.
        Gera uma lista contendo as 7 datas para as viagens.
    '''
    dates = []
    for i in range(dias):
        new_date = first_day + timedelta(days=i)
        dates.append(new_date.strftime('%Y-%m-%d'))
    return dates
