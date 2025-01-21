import pandas as pd
import sqlite3
class CreateMinardDB:
    def __init__(self):
        #讀入csv
        file_path = 'data/minard.csv'
        self.df = pd.read_csv(file_path)
    def create_city_dataframe(self):
        #選取csv中資料做成city_df
        self.city_df = self.df.iloc[:20, :3]
        return self.city_df
    def create_temperature_dataframe(self):
        #選取csv中資料做成temperature_df，合併date欄（製作新的合併資料，並刪除舊的）
        self.temperature_df = self.df.iloc[:9, 3:8]
        self.temperature_df['days'] = self.temperature_df['days'].astype(int) #float轉int
        self.temperature_df['temp'] = self.temperature_df['temp'].astype(int)
        self.temperature_df['full_date'] = self.temperature_df['date'] + ' ' + self.temperature_df['Unnamed: 7'].astype(int).astype(str)
        self.temperature_df = self.temperature_df.drop(columns=['date', 'Unnamed: 7'])
        return self.temperature_df
    def create_troop_dataframe(self):
        #選取csv中資料做成troop_df
        self.troop_df = self.df.iloc[:48, 8:13]
        return self.troop_df
    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
                    "cities": city_df,
                    "temperatures": temperature_df,
                    "troops": troop_df
                }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")
        connection.close()
create_minard_db = CreateMinardDB()
create_minard_db.create_database()