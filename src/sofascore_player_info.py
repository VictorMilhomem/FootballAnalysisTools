import pandas as pd
import requests
from datetime import datetime
import time
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import os

BASE_DIR = 'data'
RAW_DIR = os.path.join(BASE_DIR, 'raw')
ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')
IMAGES_DIR = os.path.join(ENGINEERED_DIR, 'players_images')

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

HEADERS = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.6',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"7854d9f830"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'If-Modified-Since': formatted_datetime
}


def scrape_player_info(player_id, headers=HEADERS):
    params = {
            'limit': '20',
            'order': '-rating',
        }

    response = requests.get(
            f'https://api.sofascore.app/api/v1/player/{player_id}',
            params=params,
            headers=headers,
        )
    return response

def scrape_all_league_players(players_id: list, league_id: int):
    raw_list = []
    for id in tqdm(players_id):
        player_response = scrape_player_info(id)
        data = player_response.json()
        data['player']['team'].pop('tournament', None)
        raw_list.append(data)
        time.sleep(0.5)
    return raw_list

def generate_dfs(response_list: list):
    raw_dfs = []
    for resp in response_list:
        df = pd.json_normalize(resp['player'])
        raw_dfs.append(df)
    return raw_dfs

def concat_dfs(raw_dfs: list):
    return pd.concat(raw_dfs, ignore_index=True)


def create_all_files(df: pd.DataFrame, league_id: int, ext: str = 'csv'):
    league_dir = os.path.join(RAW_DIR, f'{league_id}')
    player_dir = os.path.join(league_dir, 'players_info')
    os.makedirs(league_dir, exist_ok=True)
    os.makedirs(player_dir, exist_ok=True)
    filename = f'players_info_{league_id}.{ext}'
    filepath = os.path.join(player_dir, filename)
    if ext == 'csv':
            df.to_csv(filepath, index=False)
    elif ext == 'xls':
        df.to_excel(filepath, index=False)

def load_file(league_id, season_id, ext='csv'):
    filepath = f'data\\raw\\{league_id}\\{season_id}\\attack_{league_id}_{season_id}.{ext}'
    if ext == 'xls':
        return pd.read_excel(filepath)
    return pd.read_csv(filepath)

def run(df: pd.DataFrame, league_id):
    player_list = list(df['player.id'])
    data = scrape_all_league_players(player_list, league_id)
    raw_dfs = generate_dfs(data)
    final_df = concat_dfs(raw_dfs)
    return final_df


if __name__ == "__main__":
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(ENGINEERED_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    league_id = 325
    season_id = 48982

    brazil_df = load_file(league_id, season_id)
    brazil_df_final = run(brazil_df, league_id)
    create_all_files(brazil_df_final, league_id)

    league_id = 155
    season_id = 47647

    argentina = load_file(league_id, season_id)
    argentina_final = run(argentina, league_id)
    create_all_files(argentina_final, league_id)
    time.sleep(10)

    league_id = 16736
    season_id = 48353

    bol = load_file(league_id, season_id)
    bol_final = run(bol, league_id)
    create_all_files(bol_final, league_id)
    time.sleep(10)

    league_id = 240
    season_id = 48720

    ecuador = load_file(league_id, season_id)
    ecuador_final = run(ecuador, league_id)
    create_all_files(ecuador_final, league_id)