import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import os

BASE_DIR = 'data'
RAW_DIR = os.path.join(BASE_DIR, 'raw')
ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')

def load_dataset(filepath: str, ext: str='csv'):
    if ext == 'xls':
        return pd.read_excel(filepath)
    
    return pd.read_csv(filepath)

def clean_player_info(df: pd.DataFrame):
    columns_to_keep = df.filter(['name', 'slug', 'shortName', 'position',
       'height', 'preferredFoot', 'userCount', 'id',
       'shirtNumber', 'dateOfBirthTimestamp', 'contractUntilTimestamp','team.id',
       'proposedMarketValue','country.alpha2', 'country.name',
       'proposedMarketValueRaw.value', 'proposedMarketValueRaw.currency']
       ).columns
    df = df[columns_to_keep]
    df['dateOfBirthTimestamp'] = pd.to_datetime(df['dateOfBirthTimestamp'], unit='s')
    df['contractUntilTimestamp'] = pd.to_datetime(df['contractUntilTimestamp'], unit='s')
    df['proposedMarketValueRaw.currency'].fillna('EUR', inplace=True)
    df = df.rename(columns={'dateOfBirthTimestamp': 'dateOfBirth', 'contractUntilTimestamp': 'contractUntil', 'id':'player.id'})
    df['player.image'] = 'https://api.sofascore.app/api/v1/player/' + df['player.id'].astype(str)  + '/image'
    
    return df


def clean_teams_info(df: pd.DataFrame):
    columns_to_keep = df.filter(['name', 'slug', 'shortName', 'gender', 'userCount', 'nameCode',
       'disabled', 'national', 'type', 'id', 'fullName',
       'foundationDateTimestamp', 'sport.name', 'sport.slug', 'sport.id',
       'category.name', 'category.slug', 'category.sport.name',
       'category.sport.slug', 'category.sport.id', 'category.id',
       'category.flag', 'category.alpha2','venue.stadium.name', 'venue.stadium.capacity', 'venue.id',
       'venue.country.alpha2', 'venue.country.name', 'country.alpha2',
       'country.name', 'teamColors.primary', 'teamColors.secondary',
       'teamColors.text']
       ).columns
    df = df[columns_to_keep]
    df = df.rename(columns={ 'id':'team.id'})
    df['team.image'] = 'https://api.sofascore.app/api/v1/team/' + df['team.id'].astype(str) + '/image'
    return df


def clean_stats(df: pd.DataFrame):
    df = df.drop(['player.name', 'player.slug', 'player.userCount',
       'team.name', 'team.slug', 'team.shortName', 'team.userCount',
       'team.type', 'team.teamColors.primary',
       'team.teamColors.secondary', 'team.teamColors.text'],axis=1,)
    return df


def save_to_engineered(df: pd.DataFrame, league_id: int, folder: str,ext: str = 'csv'):
    league_dir = os.path.join(ENGINEERED_DIR, f'{league_id}')
    dir = os.path.join(league_dir, folder)
    os.makedirs(league_dir, exist_ok=True)
    os.makedirs(dir, exist_ok=True)
    filename = f'{folder}_{league_id}.{ext}'
    filepath = os.path.join(dir, filename)
    if ext == 'csv':
            df.to_csv(filepath, index=False)
    elif ext == 'xls':
        df.to_excel(filepath, index=False)

def load_file(filepath):
    return pd.read_csv(filepath)

def run(df, league_id, dataset_info):
    if dataset_info == 'player_info':
        player_info_engineered = clean_player_info(df[0])
        save_to_engineered(player_info_engineered, league_id,  'players_info')
    elif dataset_info == 'teams_info':
        team_info_engineered = clean_teams_info(df[0])
        save_to_engineered(team_info_engineered, league_id,  'teams_info')
    else:
        attack_engineered = clean_stats(df[0])
        defense_engineered = clean_stats(df[1])
        keepers_engineered = clean_stats(df[2])
        passing_engineered = clean_stats(df[3])
        others_engineered = clean_stats(df[4])
        save_to_engineered(attack_engineered, league_id,  'attack')
        save_to_engineered(defense_engineered, league_id,  'defense')
        save_to_engineered(keepers_engineered, league_id,  'keepers')
        save_to_engineered(passing_engineered, league_id,  'passing')
        save_to_engineered(others_engineered, league_id,  'others')

if __name__ == "__main__":
    league_id = 325
    season_id = 48982

    player_df = load_file(filepath = f'data\\raw\\{league_id}\\players_info\\players_info_{league_id}.csv')
    _df = [player_df]
    run(_df, league_id, 'player_info')

    attack_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\attack_{league_id}_{season_id}.csv')
    defense_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\defense_{league_id}_{season_id}.csv')
    keepers_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\keepers_{league_id}_{season_id}.csv')
    passing_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\passing_{league_id}_{season_id}.csv')
    others_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\others_{league_id}_{season_id}.csv')
    _df = [attack_df, defense_df, keepers_df, passing_df, others_df]
    run(_df, league_id, 'stats')

    team_df = load_file(filepath = f'data\\raw\\{league_id}\\teams_info\\teams_info_{league_id}.csv')
    _df = [team_df]
    run(_df, league_id, 'teams_info')

    league_id = 155
    season_id = 47647

    player_df = load_file(filepath = f'data\\raw\\{league_id}\\players_info\\players_info_{league_id}.csv')
    _df = [player_df]
    run(_df, league_id, 'player_info')

    attack_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\attack_{league_id}_{season_id}.csv')
    defense_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\defense_{league_id}_{season_id}.csv')
    keepers_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\keepers_{league_id}_{season_id}.csv')
    passing_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\passing_{league_id}_{season_id}.csv')
    others_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\others_{league_id}_{season_id}.csv')
    _df = [attack_df, defense_df, keepers_df, passing_df, others_df]
    run(_df, league_id, 'stats')

    team_df = load_file(filepath = f'data\\raw\\{league_id}\\teams_info\\teams_info_{league_id}.csv')
    _df = [team_df]
    run(_df, league_id, 'teams_info')

    league_id = 240
    season_id = 48720

    player_df = load_file(filepath = f'data\\raw\\{league_id}\\players_info\\players_info_{league_id}.csv')
    _df = [player_df]
    run(_df, league_id, 'player_info')

    attack_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\attack_{league_id}_{season_id}.csv')
    defense_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\defense_{league_id}_{season_id}.csv')
    keepers_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\keepers_{league_id}_{season_id}.csv')
    passing_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\passing_{league_id}_{season_id}.csv')
    others_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\others_{league_id}_{season_id}.csv')
    _df = [attack_df, defense_df, keepers_df, passing_df, others_df]
    run(_df, league_id, 'stats')

    team_df = load_file(filepath = f'data\\raw\\{league_id}\\teams_info\\teams_info_{league_id}.csv')
    _df = [team_df]
    run(_df, league_id, 'teams_info')

    league_id = 16736
    season_id = 48353

    player_df = load_file(filepath = f'data\\raw\\{league_id}\\players_info\\players_info_{league_id}.csv')
    _df = [player_df]
    run(_df, league_id, 'player_info')

    attack_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\attack_{league_id}_{season_id}.csv')
    defense_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\defense_{league_id}_{season_id}.csv')
    keepers_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\keepers_{league_id}_{season_id}.csv')
    passing_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\passing_{league_id}_{season_id}.csv')
    others_df = load_file(f'data\\raw\\{league_id}\\{season_id}\\others_{league_id}_{season_id}.csv')
    _df = [attack_df, defense_df, keepers_df, passing_df, others_df]
    run(_df, league_id, 'stats')

    team_df = load_file(filepath = f'data\\raw\\{league_id}\\teams_info\\teams_info_{league_id}.csv')
    _df = [team_df]
    run(_df, league_id, 'teams_info')