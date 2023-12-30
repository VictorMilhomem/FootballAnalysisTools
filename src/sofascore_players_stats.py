import pandas as pd
import requests
from datetime import datetime
from tqdm import tqdm
import os

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


ATRB = {
    'attack': 'goals,successfulDribblesPercentage,blockedShots,penaltyWon,goalsFromOutsideTheBox,hitWoodwork,expectedGoals,totalShots,goalConversionPercentage,shotFromSetPiece,headedGoals,offsides,bigChancesMissed,shotsOnTarget,penaltiesTaken,freeKickGoal,leftFootGoals,penaltyConversion,successfulDribbles,shotsOffTarget,penaltyGoals,goalsFromInsideTheBox,rightFootGoals,setPieceConversion,rating',
    'defense': 'tackles,errorLeadToGoal,cleanSheet,interceptions,errorLeadToShot,penaltyConceded,ownGoals,clearances,dribbledPast,rating',
    'passing': 'bigChancesCreated,totalPasses,accurateFinalThirdPasses,accurateLongBalls,assists,accuratePassesPercentage,keyPasses,accurateLongBallsPercentage,accuratePasses,accurateOwnHalfPasses,accurateCrosses,passToAssist,inaccuratePasses,accurateOppositionHalfPasses,accurateCrossesPercentage,rating',
    'keepers': 'saves,savedShotsFromInsideTheBox,punches,crossesNotClaimed,cleanSheet,savedShotsFromOutsideTheBox,runsOut,penaltyFaced,goalsConcededInsideTheBox,successfulRunsOut,penaltySave,goalsConcededOutsideTheBox,highClaims,rating',
    'others': 'yellowCards,aerialDuelsWon,minutesPlayed,possessionLost,redCards,aerialDuelsWonPercentage,wasFouled,appearances,groundDuelsWon,totalDuelsWon,fouls,matchesStarted,groundDuelsWonPercentage,totalDuelsWonPercentage,dispossessed,rating'
}

FILTERS = 'position.in.G~D~M~F'


FILES_NAMES = {
    0: 'attack',
    1: 'defense', 
    2: 'passing', 
    3: 'keepers',
    4: 'others',
}


def scrape_tournament_players_stats(id, season_id, headers=HEADERS, atr='attack', filters=FILTERS, offset=0):
    
    params = {
        'limit': '20',
        'order': '-rating',
        'accumulation': 'total',
        'fields': ATRB[atr],
        'filters': filters,
    }

    if offset > 0 :
        params['offset'] = str(offset)
        
    response = requests.get(
        f'https://api.sofascore.com/api/v1/unique-tournament/{id}/season/{season_id}/statistics',
        params=params,
        headers=headers,
    )
    return response

def scrape_all_pages(id, season_id, atr='attack', pages=37):
    response_list = []
    offset=0
    while True:

        resp = scrape_tournament_players_stats(id, season_id, atr=atr, offset=offset)
        if offset <= pages*20:
            response_list.append(resp)
            offset += 20
            
        else:
            break
    return response_list

def scrape_all_atr(id, season_id, pages=37):
    response_list = []
    for key, _ in ATRB.items():
        resp = scrape_all_pages(id, season_id, atr=key, pages=pages)
        response_list.append(resp)
    return response_list


def generate_dfs(response_list: list):
    raw_dfs = []
    for resp in response_list:
        raw_json = resp.json()
        df = pd.json_normalize(raw_json['results'])
        raw_dfs.append(df)
    return raw_dfs

def generate_single_df(response):
    return pd.json_normalize(response.json()['results'])


def join_same_atr_df(dfs: list):
    return pd.concat(dfs, ignore_index=True)


BASE_DIR = 'data'
RAW_DIR = os.path.join(BASE_DIR, 'raw')
ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')

def create_all_stats_files(dfs: pd.DataFrame, filenames: dict, id: int, season_id: int, ext: str):
    for i, base_name in filenames.items():
        df = dfs[i]
        filename = f'{base_name}_{id}_{season_id}.{ext}'
        league_dir = os.path.join(RAW_DIR, f'{id}')
        season_dir = os.path.join(league_dir, f'{season_id}')
        os.makedirs(league_dir, exist_ok=True)
        os.makedirs(season_dir, exist_ok=True)
        filepath = os.path.join(season_dir, filename)
        if ext == 'csv':
            df.to_csv(filepath, index=False)
        elif ext == 'xls':
            df.to_excel(filepath, index=False)
        else: raise TypeError('Unsupported File Type')

def run(league_id, season_id, pages=37):
    data = scrape_all_atr(id=league_id, season_id=season_id, pages=pages)
    final_df = []
    for i in range(len(data)):
        dfs = generate_dfs(data[i])
        df = join_same_atr_df(dfs)
        final_df.append(df)
    return final_df

if __name__ == "__main__":
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(ENGINEERED_DIR, exist_ok=True)

    league_id = 325
    season_id = 48982

    brazil_dfs = run(league_id, season_id)
    create_all_stats_files(brazil_dfs, FILES_NAMES, league_id, season_id, 'csv')

    league_id = 155
    season_id = 47647

    argentina_dfs = run(league_id, season_id, pages=42)
    create_all_stats_files(argentina_dfs, FILES_NAMES, league_id, season_id, 'csv')

    league_id = 16736
    season_id = 48353

    bol_dfs = run(league_id, season_id, pages=28)
    create_all_stats_files(bol_dfs, FILES_NAMES, league_id, season_id, 'csv')

    league_id = 240
    season_id = 48720

    ecuador = run(league_id, season_id, pages=25)
    create_all_stats_files(ecuador, FILES_NAMES, league_id, season_id, 'csv')