import requests
import time
from colorama import Fore, Style

def chiedi_api_key():
    return input(f"{Fore.GREEN}Inserisci il token API del tuo bot Telegram e imposta il bot come admin in un gruppo.\n\nIn questo modo sarai in grado di leggere le conversazioni da terminale e visualizzare anche i messaggi eliminati. Inoltre, potrai visualizzare il numero ID dell'utente\n\nCreato da t.me/VikingTerminalInserisci API KEY del bot: {Fore.RESET}")

TELEGRAM_BOT_TOKEN = chiedi_api_key()

def leggi_aggiornamenti(offset=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(url, params=params)
    return response.json()

def ottieni_ultimo_update_id():
    aggiornamenti = leggi_aggiornamenti()
    tutti_gli_id = [aggiornamento['update_id'] for aggiornamento in aggiornamenti['result']] if 'result' in aggiornamenti else []
    return max(tutti_gli_id) if tutti_gli_id else None

def main():
    print(f"{Fore.GREEN}Inizializzazione del bot...{Fore.RESET}")
    ultimo_update_id = ottieni_ultimo_update_id()  
    offset = ultimo_update_id + 1 if ultimo_update_id is not None else None

    while True:
        try:
            aggiornamenti = leggi_aggiornamenti(offset)

            if 'result' in aggiornamenti and aggiornamenti['result']:
                for aggiornamento in aggiornamenti['result']:
                    chat_id = aggiornamento['message']['chat']['id']
                    username = aggiornamento['message']['chat']['username'] if 'username' in aggiornamento['message']['chat'] else ''
                    user_id = aggiornamento['message']['from']['id'] if 'from' in aggiornamento['message'] else ''
                    messaggio_testo = aggiornamento['message']['text'] if 'text' in aggiornamento['message'] else 'Non è un testo'

                    print(f"{Fore.GREEN}Messaggio ricevuto da {Fore.CYAN}{username or user_id} ({chat_id}){Fore.RESET}: {messaggio_testo}")

                    offset = aggiornamento['update_id'] + 1

        except Exception as e:
            print(f"{Fore.RED}Errore: {e}{Fore.RESET}")

        time.sleep(1)

if __name__ == "__main__":
    main()
