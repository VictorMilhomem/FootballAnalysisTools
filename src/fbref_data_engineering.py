import pandas as pd
import os
from utils import BASE_FOLDER

BASE_DIR = os.path.join(BASE_FOLDER, 'data')
RAW_DIR = os.path.join(BASE_DIR, 'raw')
ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')
YEAR = '2024'
SEASON_DIR = os.path.join(ENGINEERED_DIR, YEAR)
PLAYERS_DIR = os.path.join(SEASON_DIR, 'players_stats')


PLAYERS_DICT = [
        "advanced goalkeeping",
        "defensive",
        "goal and shot creation",
        "goalkeeping",
        "misc",
        "pass types",
        "passing",
        "playing time",
        "possession",
        "shooting",
        "standard",
]


output_dir = os.path.join(ENGINEERED_DIR, YEAR, 'players_stats')
input_dir_europe = os.path.join(RAW_DIR, '2023-2024')
input_dir_south_america = os.path.join(RAW_DIR, YEAR)
def process_folder(folder_path):
    folder_dict = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)

        folder_dict.append(df)

    return folder_dict

def process_folders(root_folder):
    folder_dicts = {}

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)

        if os.path.isdir(folder_path):
            folder_dict = process_folder(folder_path)
            folder_dicts[folder_name] = folder_dict

    return folder_dicts


dicts_europe = process_folders(input_dir_europe)
dicts_sa = process_folders(input_dir_south_america)


big_5_combined = dicts_europe["Big 5 combined"]
bundesliga_2 = dicts_europe["2. Bundesliga"]
efl_championship = dicts_europe["EFL Championship"]
eredivisie = dicts_europe["Eredivisie"]
jupiler = dicts_europe["Belgian Pro League"]
laliga_2 = dicts_europe["La Liga 2"]
liga_mx = dicts_europe["Liga MX"]
ligue_2 = dicts_europe["Ligue 2"]
primeira_liga = dicts_europe["Primeira Liga"]
serie_b = dicts_europe["Serie B"]
brazil_serie_a = dicts_sa["Brazilian Serie A"]
argentina = dicts_sa["Argentina Liga Profesional"]

final_df = {}
for i in range(len(big_5_combined)):
    to_concat = []
    to_concat.append(big_5_combined[i])
    to_concat.append(bundesliga_2[i])
    to_concat.append(efl_championship[i])
    to_concat.append(eredivisie[i])
    to_concat.append(jupiler[i])
    to_concat.append(laliga_2[i])
    to_concat.append(liga_mx[i])
    to_concat.append(ligue_2[i])
    to_concat.append(primeira_liga[i])
    to_concat.append(serie_b[i])
    to_concat.append(brazil_serie_a[i])
    to_concat.append(argentina[i])
    final_df[PLAYERS_DICT[i]] = pd.concat(to_concat, axis=0)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for key, val in final_df.items():
    file_path = os.path.join(output_dir, key + ".csv")
    val.to_csv(file_path, index=False)

stats_df = {}

for f in os.listdir(PLAYERS_DIR):
    filepath = os.path.join(PLAYERS_DIR, f)
    print(filepath)
    df = pd.read_csv(filepath)
    stats_df[f.split('.')[0]] = df


PLAYERS_DICT = [
        "standard",
        "defensive",
        "goal and shot creation",   
        "misc",
        "pass types",
        "passing",
        "playing time",
        "possession",
        "shooting",
        "advanced goalkeeping",
        "goalkeeping",
]

standard = stats_df[PLAYERS_DICT[0]]
defensive = stats_df[PLAYERS_DICT[1]]
goal = stats_df[PLAYERS_DICT[2]]
misc = stats_df[PLAYERS_DICT[3]]
pass_types = stats_df[PLAYERS_DICT[4]]
passing = stats_df[PLAYERS_DICT[5]]
playing_time = stats_df[PLAYERS_DICT[6]]
possession = stats_df[PLAYERS_DICT[7]]
shooting = stats_df[PLAYERS_DICT[8]]
adv_goalkeeper = stats_df[PLAYERS_DICT[9]]
goalkeeper = stats_df[PLAYERS_DICT[10]]


def join_dfs(left: pd.DataFrame, right: pd.DataFrame):
    columns_to_filter = list(right.columns.difference(left.columns))
    columns_to_filter.append('Player ID_')
    r = right.filter(columns_to_filter).copy()
    return pd.merge(left=left, right=r, how="left", on="Player ID_")


df_1 = join_dfs(standard, defensive)
df_2 = join_dfs(df_1, goal)
df_3 = join_dfs(df_2, misc)
df_4 = join_dfs(df_3, pass_types)
df_5 = join_dfs(df_4, passing)
df_6 = join_dfs(df_5, playing_time)
df_7 = join_dfs(df_6, possession)
df_8 = join_dfs(df_7, shooting)
df_9 = join_dfs(df_8, adv_goalkeeper)
final_df = join_dfs(df_9, goalkeeper)
final_df.drop_duplicates(inplace=True, subset=['Player ID_'])

final_df['Age'] = final_df['Age'].str.split('-').str[0].astype(float)

final_df.to_parquet(os.path.join(PLAYERS_DIR, 'merged_df.parquet'), index=False)