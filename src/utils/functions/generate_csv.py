import csv
import os
from configs.logger import logger

def generate_csv(file_name: str, trips: dict):
    # Garante que a pasta 'files' exista
    os.makedirs('files', exist_ok=True)

    # Define o caminho do arquivo CSV
    path = f'files/{file_name}.csv'

    # Cria e escreve no arquivo CSV
    with open(path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Escreve o cabeçalho
        writer.writerow([
            "Dia", "Classe", "Origem", "Destino", 
            "Preço", "Horário Saída", "Horário Chegada"
        ])

        # Escreve cada viagem
        for day, trip_list in trips.items():
            for trip in trip_list:
                writer.writerow([
                    day,
                    trip.get('trip_class').upper(),
                    trip.get('origin'),
                    trip.get('destiny'),
                    f"{trip.get('price'):.2f}",
                    trip.get('departure_time'),
                    trip.get('departure_arrival')
                ])

    logger.info(f"CSV gerado em: {path}")
