import sys
import traceback
import ScraperFC as sfc

import pandas as pd
import os
from utils import BASE_FOLDER



class FbrefScraper:

    PLAYERS_DICT = [
        "standard",
        "advanced goalkeeping",
        "defensive",
        "goal and shot creation",
        "goalkeeping",
        "misc",
        "pass types",
        "passing",
        "playing time",
        "possession",
        "shooting"
    ]

    BASE_DIR = os.path.join(BASE_FOLDER, 'data')
    RAW_DIR = os.path.join(BASE_DIR, 'raw')
    ENGINEERED_DIR = os.path.join(BASE_DIR, 'engineered')

    def __init__(self, comp_name, season="2024") -> None:
        self.season = season
        self.comp_name = comp_name
        self.SEASON_DIR = os.path.join(self.RAW_DIR, str(season))
        self.COMP_DIR = os.path.join(self.SEASON_DIR, self.comp_name)


    def contain_unnamed_level(self, level) -> bool:
        str_level = f'{level}'
        if 'Unnamed:' in str_level:
            return True
        return False


    def remove_level_columns(self, df) -> list:
        return [f'{level}_{column}' if not self.contain_unnamed_level(level) else column for level, column in df.columns.to_flat_index()]


    def generate_raw_dataframes(self, data):
        raw = []
        for stats in self.PLAYERS_DICT:
            raw.append(pd.DataFrame(data[stats][2]))
        return raw

    def generate_dataframes(self, dataframes: list) -> list:
        dfs = []
        for tb in dataframes:
                if isinstance(tb.keys(), pd.core.indexes.multi.MultiIndex):
                    tb.columns = self.remove_level_columns(tb)
                _tb = self.__clean_std_stats(tb)           
                dfs.append(_tb)
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
        
        return named_dataframes


    def generate_files(self, dir: str, dfs: list, filenames: str):
        named_dataframes = self.file_names(dfs, filenames)
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass
        self.save_to_csv(named_dataframes, dir)

    # Private functions
    def __clean_std_stats(self, dataframe):
        data = dataframe.copy()
        data.drop(['Matches'], axis=1, inplace=True)
        data['Nation'] = data['Nation'].str.replace(r'[a-z]+', '', regex=True)
        data['Nation']= data['Nation'].str.strip()
        data['Nation'].fillna('Unknown')
        data['Competition'] = self.comp_name

        return data

    def run(self):
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        if not os.path.exists(self.RAW_DIR):
            os.mkdir(self.RAW_DIR)
        if not os.path.exists(self.SEASON_DIR):
            os.mkdir(self.SEASON_DIR)
        if not os.path.exists(self.COMP_DIR):
            os.mkdir(self.COMP_DIR)
        file_names = [filename + ".csv" for filename in self.PLAYERS_DICT]
        dir = self.COMP_DIR
        scraper = sfc.FBref()
        data = None
        try:
            data = scraper.scrape_all_stats(year=self.season, league=self.comp_name)
        except:
            # Catch and print any exceptions.
            traceback.print_exc()
        
        raw_data = self.generate_raw_dataframes(data)
        engineered_data = self.generate_dataframes(raw_data)
        self.generate_files(dir, engineered_data, file_names)
        



if __name__ == "__main__":

    """
    scrape = FbrefScraper(comp_name="Brazilian Serie A", season="2024")
    scrape.run() 


    scrape = FbrefScraper(comp_name="Argentina Liga Profesional", season="2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Liga MX", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Primeira Liga", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Big 5 combined", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Eredivisie", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Belgian Pro League", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="EFL Championship", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="La Liga 2", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="2. Bundesliga", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Ligue 2", season="2023-2024")
    scrape.run()

    scrape = FbrefScraper(comp_name="Serie B", season="2023-2024")
    scrape.run()
    """
    
