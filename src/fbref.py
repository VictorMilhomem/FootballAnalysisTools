import sys
import time
from bs4 import BeautifulSoup
import requests
from tqdm.notebook import tqdm

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from scipy import stats
import math
import os
from mplsoccer import PyPizza, add_image
from highlight_text import fig_text
import warnings
import matplotlib.font_manager as fm
warnings.filterwarnings("ignore", category=FutureWarning)

class FbrefScraper:
    ADV_COMP_FILE_NAMES = [
            'championship.csv'  ,
            'home_away.csv' ,
            'squad_std_stats.csv' ,
            'squad_std_opponent_stats.csv' ,
            'squad_goalkeeping_stats.csv' ,
            'squad_goalkeeping_opponent_stats.csv' ,
            'squad_adv_goalkeeping_stats.csv' ,
            'squad_adv_goalkeeping_opponent_stats.csv' ,
            'squad_shooting_stats.csv' ,
            'squad_shooting_opponent_stats.csv' ,
            'squad_passing_stats.csv',
            'squad_passing_opponent_stats.csv',
            'squad_passtypes_stats.csv',
            'squad_passtypes_opponent_stats.csv',
            'squad_goal_shoot_creation_stats.csv',
            'squad_goal_shoot_creation_opponent_stats.csv',
            'squad_defensive_stats.csv',
            'squad_defensive_opponent_stats.csv',
            'squad_possesion_stats.csv',
            'squad_possesion_opponent_stats.csv',
            'squad_playingtime_stats.csv',
            'squad_playingtime_opponent_stats.csv',
            'squad_miscellaneous_stats.csv',
            'squad_miscellaneous_opponent_stats.csv',
    ]

    ADV_TEAMS_FILE_NAMES = [
        'squad_std_stats.csv',
        'score_fixtures.csv',
        'squad_goalkeeping_stats.csv',
        'squad_adv_goalkeeping_stats.csv',
        'squad_shooting_stats.csv',
        'squad_passing_stats.csv',
        'squad_passtypes_stats.csv',
        'squad_goal_shoot_creation_stats.csv',
        'squad_defensive_stats.csv',
        'squad_possesion_stats.csv',
        'squad_playingtime_stats.csv',
        'squad_miscellaneous_stats.csv',
        'regular_season.csv',
        'home_away.csv'
    ]

    SIMPLE_TEAMS_FILE_NAMES = [
        'squad_std_stats.csv',
        'score_fixtures.csv',
        'squad_goalkeeping_stats.csv',
        'squad_shooting_stats.csv',
        'squad_playingtime_stats.csv',
        'squad_miscellaneous_stats.csv',
        'regular_season.csv',
    ]

    CHAMPIONSHIP = None

    DIR = {
        9: 'premier_league',
        10: 'english_championship',
        11: 'italian_serie_A',
        12: 'laliga',
        13: 'ligue1',
        17: 'spanish_second_division',
        18: 'italian_serie_B',
        20: 'bundesliga',
        21: 'primera_division_argentina',
        22: 'mls',
        23: 'eredivisie',
        24: 'brazil_serie_A',
        31: 'liga_mx',
        32: 'primeira_liga_portugal',
        33: '2bundesliga',
        37: 'belgium_pro',
        60: 'ligue2',
        # without advanced stats
        15:'efl_league_one',
        16:'efl_league_two',
        35: 'chile_primera_division',
        38: 'brazil_serie_B',
        41: 'colombian_primera_division',
        50: 'denish_first',
        25: 'j1_league',
        70: 'saudi_first'
    }

    LEAGUES_WITHOUT_ADV_STATS = [15, 16, 35, 38, 41, 50, 25, 70]

    BASE_DIR = os.path.join('..', 'data')
    RAW_DIR = os.path.join(BASE_DIR, 'raw')
    ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')

    def __init__(self, comp_id, season='2023') -> None:
        self.season = season
        self.CHAMPIONSHIP = {
                            9:  f'https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats',
                            10: f'https://fbref.com/en/comps/10/{season}/{season}-Championship-Stats',
                            11: f'https://fbref.com/en/comps/11/{season}/{season}-Serie-A-Stats',
                            12: f'https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats',
                            13: f'https://fbref.com/en/comps/13/{season}/{season}-Ligue-1-Stats',
                            17: f'https://fbref.com/en/comps/17/{season}/{season}-Segunda-Division-Stats',
                            18: f'https://fbref.com/en/comps/18/{season}/{season}-Serie-B-Stats',
                            20: f'https://fbref.com/en/comps/20/{season}/{season}-Bundesliga-Stats',
                            21: f'https://fbref.com/en/comps/21/{season}/{season}-Primera-Division-Stats',
                            22: f'https://fbref.com/en/comps/22/{season}/{season}-Major-League-Soccer-Stats',
                            23: f'https://fbref.com/en/comps/23/{season}/{season}-Eredivisie-Stats',
                            24: f'https://fbref.com/en/comps/24/{season}/{season}-Serie-A-Stats',
                            31: f'https://fbref.com/en/comps/31/{season}/{season}-Liga-MX-Stats',
                            32: f'https://fbref.com/en/comps/32/{season}/{season}-Primeira-Liga-Stats',
                            33: f'https://fbref.com/en/comps/33/{season}/{season}-2-Bundesliga-Stats',
                            37: f'https://fbref.com/en/comps/37/{season}/{season}-Belgian-Pro-League-Stats',
                            60: f'https://fbref.com/en/comps/60/{season}/{season}-Ligue-2-Stats',

                            # without advanced stats
                            15: f'https://fbref.com/en/comps/15/{season}/{season}-League-One-Stats',
                            16: f'https://fbref.com/en/comps/16/{season}/{season}-League-Two-Stats',
                            35: f'https://fbref.com/en/comps/35/{season}/{season}-Primera-Division-Stats',
                            38: f'https://fbref.com/en/comps/38/{season}/{season}-Serie-B-Stats',
                            41: f'https://fbref.com/en/comps/41/{season}/{season}-Primera-A-Stats',
                            50: f'https://fbref.com/en/comps/50/{season}/{season}-Superliga-Stats',
                            25: f'https://fbref.com/en/comps/25/{season}/{season}-J1-League-Stats',
                            70: f'https://fbref.com/en/comps/70/{season}/{season}-Saudi-Professional-League-Stats'
                        }
        self.comp_id = comp_id
        self.comp_url = self.CHAMPIONSHIP[comp_id]
        self.comp_dir = self.DIR[comp_id]
        self.SEASON_DIR = os.path.join(self.RAW_DIR, str(season))
        self.COMP_DIR = os.path.join(self.SEASON_DIR, self.comp_dir)

    def get_teams_urls(self, comp_url):
        request = requests.get(comp_url)
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        hrefs = {}
        base_url = 'https://fbref.com'
        for row in table.find_all('tr'):
            try:
                tr = row.select_one('td:nth-child(2) > a')
                href = str(tr.get('href'))
                team_url = base_url + href
                team = tr.text
                hrefs[team] = team_url
            except:
                pass
            
        return hrefs

    def contain_unnamed_level(self, level) -> bool:
        str_level = f'{level}'
        if 'Unnamed:' in str_level:
            return True
        return False


    def remove_level_columns(self, df) -> list:
        return [f'{level}_{column}' if not self.contain_unnamed_level(level) else column for level, column in df.columns.to_flat_index()]


    def generate_dataframes(self, web_page: list) -> list:
        dfs = []
        for tb in web_page:
            if isinstance(tb.keys(), pd.core.indexes.multi.MultiIndex):
                tb.columns = self.remove_level_columns(tb)
            dfs.append(tb)
        return dfs


    def save_to_csv(self, dataframes: dict, path):
        for file_name, dataframe in dataframes.items():
            file_path = os.path.join(path, file_name)
            try:
                dataframe.to_csv(file_path, index=False, encoding="utf-8")
            except FileNotFoundError:
                sys.exit(64)


    def file_names(self, dfs: list, filenames: list) -> dict:
        named_dataframes = {}
        size = len(dfs)
        if size == len(filenames):
            for i in range(size):
                filename = filenames[i]
                named_dataframes[filename] = dfs[i]
        else:
            for i in range(size):
                filename = str(i) + ".csv"
                named_dataframes[filename] = dfs[i]
        
        return named_dataframes


    def generate_files(self, dir: str, dfs: list, filenames: str):
        named_dataframes = self.file_names(dfs, filenames)
        
        dirname = os.path.join(self.COMP_DIR, dir)

        try:
            os.mkdir(dirname)
        except FileExistsError:
            pass
        self.save_to_csv(named_dataframes, dirname)

    # Private functions
    def __clean_std_stats(self, data):
        data.drop(['Matches'], axis=1, inplace=True)
        data['Nation'] = data['Nation'].str.replace(r'[a-z]+', '', regex=True)
        data['Nation']= data['Nation'].str.strip()
        data['Nation'].fillna('Unknow')

        # drop total lines
        data  = data[~data['Player'].str.contains('Squad Total')]
        data  = data[~data['Player'].str.contains('Opponent Total')]

        #cleaning age column
        data['Age'] = data['Age'].astype(str)
        data['Age'] = data['Age'].str.replace(r'-[0-9]+', '', regex=True)
        data['Age']= data['Age'].str.strip()
        data['Age'] = pd.to_numeric(data['Age'], errors='coerce')

        if 'Playing Time_MP' in data.columns:
            data = data.rename(columns={'Playing Time_MP': 'MP'})

        data.iloc[:, 4:33] = data.iloc[:, 4:33].fillna(0)

        return data

    def __add_team_championship(self, data, team, championship):
        data['Team'] = team
        data['Championship'] = championship
        data['Player_Team'] = data['Player'] + ' (' + data['Team'] + ')'
        return data
    
    def __directories(self, folder_path):
        entries = os.listdir(folder_path)
        directories = (entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry)))
        directory_names = list(directories)

        return directory_names

    def __read_files(self, output_path, filename):
        datas = []
        teams = []
        folders = self.__directories(output_path)
        for folder in folders:
            team_folder = os.path.join(output_path, folder)
            teams.append(folder.split('_')[0])

            file_path = os.path.join(team_folder, filename)
            df = pd.read_csv(file_path)
            datas.append(df)
        return datas, teams
    
    def __transform(self, datas, teams, champ='Brasileiro'):
        new_datas = []
        for i in range(len(datas)):
            data = datas[i]
            team = teams[i]
            data = self.__clean_std_stats(data)
            data = self.__add_team_championship(data, team, champ)
            new_datas.append(data)
        return new_datas
    
    def __concat_dfs(self, datas):
        df_combined = pd.concat(datas, ignore_index=True)
        return df_combined
    
    def __run_data_transform(self):
        for file in self.ADV_TEAMS_FILE_NAMES:
            if not file in ['regular_season.csv', 'score_fixtures.csv', 'home_away.csv']:
                datas, teams = self.__read_files(self.COMP_DIR, file)
                new = self.__transform(datas, teams)
                transformed_df = self.__concat_dfs(new)
                season_dir = os.path.join(self.ENGINEERED_DIR, self.season)
                comp_dir = os.path.join(season_dir, self.comp_dir)
                filepath = os.path.join(comp_dir, file)
                if not os.path.exists(self.ENGINEERED_DIR):
                    os.mkdir(self.ENGINEERED_DIR)
                if not os.path.exists(season_dir):
                    os.mkdir(season_dir)
                if not os.path.exists(comp_dir):
                    os.mkdir(comp_dir)
                transformed_df.to_csv(filepath, index=False)


    def run(self, squad_stats=True, transform=True):
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        if not os.path.exists(self.RAW_DIR):
            os.mkdir(self.RAW_DIR)
        if not os.path.exists(self.SEASON_DIR):
            os.mkdir(self.SEASON_DIR)
        if not os.path.exists(self.COMP_DIR):
            os.mkdir(self.COMP_DIR)
        urls = self.get_teams_urls(self.comp_url) if squad_stats else self.comp_url
        if squad_stats:
            file_names = self.SIMPLE_TEAMS_FILE_NAMES if self.comp_id in self.LEAGUES_WITHOUT_ADV_STATS else self.ADV_TEAMS_FILE_NAMES
        else:
            file_names = self.ADV_COMP_FILE_NAMES
        dir = self.comp_dir
        for dir, url in tqdm(urls.items()):
            web_page = pd.read_html(url)
            dfs = self.generate_dataframes(web_page)
            self.generate_files(dir, dfs, file_names)
            time.sleep(0.5)
        if transform and  not (self.comp_id in self.LEAGUES_WITHOUT_ADV_STATS):
            self.__run_data_transform()

class SoccerPlot:
    font_normal = os.path.join('..', 'fonts', 'Lora-VariableFont_wght.ttf')
    font_italic = os.path.join('..', 'fonts', 'Lora-Italic-VariableFont_wght.ttf')
    font_bold = os.path.join('..', 'fonts', 'Oswald-VariableFont_wght.ttf')
    font_normal_prop = fm.FontProperties(fname=font_normal)
    font_italic_prop = fm.FontProperties(fname=font_italic)
    font_bold_prop = fm.FontProperties(fname=font_bold)

    def __init__(self, df, cols_filter) -> None:
        self.df = df
        self.cols_filter = cols_filter

    def get_player(self, player_name, dataframe, cols_filter):
        player = dataframe.loc[(dataframe['Player'] == player_name)].reset_index()
        player = player[cols_filter]
        return list(player.loc[0])

    def calculate_percintiles(self, params, dataframe, player):
        values = []
        for x in range(len(params)):
            values.append(math.floor(stats.percentileofscore(dataframe[params[x]], player[x])))
        return values

    def get_params_list(self, df: pd.DataFrame, cols_filter):
        params_df = df[cols_filter]
        params = list(params_df.columns)
        return params
    
    def round_image(self, img):
        width, height = img.size

        # Create a circular mask with a perfect circle
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        min_dim = min(width, height)
        circle_radius = min_dim // 2
        circle_center = (width // 2, height // 2)
        
        draw.ellipse([(circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                    (circle_center[0] + circle_radius, circle_center[1] + circle_radius)],
                    fill=255)
        result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        result.paste(img, (0, 0), mask)

        return result
    
    def create_simple_pizza_plot(self, values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):

        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=20            # increase the circle size
        )
        slice_colors = [color_palette["color2"]]*len(self.cols_filter)
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors,
            value_bck_colors=slice_colors,
            color_blank_space="same",
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette['color2'],
                    boxstyle="round,pad=0.2", lw=1
                )
            )                    # values to be used when adding parameter-values
        )

        # add title
        fig.text(
            0.515, 0.975, title, size=16,
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.953,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )
        # add image
        if (player_image != None) and (team_image != None):
            player_image = self.round_image(player_image)
            ax_image = add_image(player_image, fig, left=0.4, bottom=0.38, width=0.224, height=0.228)
            ax_image = add_image(team_image, fig, left=0., bottom=0.9, width=0.1, height=0.1)

        return fig, ax
    
    
    def create_3_pilars_pizza_plot(self, values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette: dict):
        """
        Create a pizza plot with 3 categories with 5 Stats for each
        """
        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=20            # increase the circle size
        )
        slice_colors = [color_palette["color1"]]*5 + [color_palette["color2"]]*5 + [color_palette["color3"]] * 5
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors,
            value_bck_colors=slice_colors,
            color_blank_space="same",
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000",
                    boxstyle="round,pad=0.2", lw=1
                )
            )                    # values to be used when adding parameter-values
        )

        # add title
        fig.text(
            0.515, 0.975, title, size=16,
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.953,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )
        # add image
        if (player_image != None) and (team_image != None):
            player_image = self.round_image(player_image)
            ax_image = add_image(player_image, fig, left=0.4, bottom=0.38, width=0.224, height=0.228)
            ax_image = add_image(team_image, fig, left=0., bottom=0.9, width=0.1, height=0.1)

        return fig, ax
    
    def create_compare_pizza_plot(self, values, values_2, params, title, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette: dict):

        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of params
            background_color=color_palette["bkg"],
            straight_line_color="#000000",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=1,               # linewidth of last circle
            other_circle_lw=1,              # linewidth for other circles
            other_circle_ls="-.",           # linestyle for other circles
            inner_circle_size=10           # increase the circle size
        )
        slice_colors_player1 = [color_palette["color1"]]*len(self.cols_filter)
        # plot pizza
        fig, ax = baker.make_pizza(
            values,              # list of values
            compare_values=values_2,
            figsize=(8, 8),      # adjust figsize according to your need
            slice_colors=slice_colors_player1,
            value_bck_colors=slice_colors_player1,
            param_location=110,  # where the parameters will be added
            kwargs_slices=dict(
                edgecolor="#000000",
                zorder=2, linewidth=1
            ),                   # values to be used when plotting slices
            kwargs_compare=dict(
                facecolor=color_palette["color2"], edgecolor="#000000",
                zorder=2, linewidth=1,
            ),
            kwargs_params=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                va="center"
            ),                   # values to be used when adding parameter
            kwargs_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette["color1"],
                    boxstyle="round,pad=0.2", lw=1
                )
            ) ,                   # values to be used when adding parameter-values
            kwargs_compare_values=dict(
                color="#F2F2F2", fontsize=12,
                fontproperties=self.font_normal_prop,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor=color_palette["color2"],
                    boxstyle="round,pad=0.2", lw=1
                )
            )
        )

        # add title
        fig_text(
            0.515, 0.99, title, size=16, fig=fig,
            highlight_textprops=[{"color": color_palette["color1"]}, {"color": color_palette["color2"]}],
            ha="center", fontproperties=self.font_bold_prop, 
            color="#F2F2F2"
        )

        # add subtitle
        fig.text(
            0.515, 0.942,
            subtitle,
            size=13,
            ha="center", fontproperties=self.font_bold_prop,
            color="#F2F2F2"
        )

        fig.text(
            0.99, 0.02, f"{data_credit}\n{your_credit}", size=9,
            fontproperties=self.font_italic_prop,
            color="#F2F2F2",
            ha="right"
        )

        if (player1_image != None) and (player2_image != None):
            player1_image = self.round_image(player1_image)
            player2_image = self.round_image(player2_image)
            ax_image = add_image(player2_image, fig, left=0.8, bottom=0.8, width=0.224, height=0.228)
            ax_image = add_image(player1_image, fig, left=0., bottom=0.8, width=0.224, height=0.228)

        return fig, ax
    
    def generate_simple_pizza_plot(self, player_name, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player = self.get_player(player_name, self.df, self.cols_filter)
        values = self.calculate_percintiles(params, self.df, player)

        self.create_simple_pizza_plot(values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette)
        plt.show()

    def generate_3_pilars_pizza_plot(self, player_name, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette:dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player = self.get_player(player_name, self.df, self.cols_filter)
        values = self.calculate_percintiles(params, self.df, player)

        self.create_3_pilars_pizza_plot(values, params, title, subtitle, data_credit, your_credit, player_image, team_image, color_palette)
        plt.show()
    
    def generate_compare_pizza_plot(self, player_name1, player_name2, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette: dict):
        params = self.get_params_list(self.df, self.cols_filter)
        player_1 = self.get_player(player_name1, self.df, self.cols_filter)
        values_1 = self.calculate_percintiles(params, self.df, player_1)

        player_2 = self.get_player(player_name2, self.df, self.cols_filter)
        values_2 = self.calculate_percintiles(params, self.df, player_2)

        title = f'<{player_name1}> vs <{player_name2}>'
        self.create_compare_pizza_plot(values_1, values_2,params, title, subtitle, data_credit, your_credit, player1_image, player2_image, color_palette)
        plt.show()


if __name__ == "__main__":
    brazil_id = 24
    scrape = FbrefScraper(comp_id=brazil_id)
    urls = scrape.run(squad_stats=True)