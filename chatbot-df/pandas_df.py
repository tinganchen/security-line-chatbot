import pandas as pd
import datetime

def get_current_time():
    return str(datetime.datetime.now())[:19]

class log:
    def __init__(self):
        self.df = None
        self.columns = ['UserID', 'Time', 'Service', 'Message']

        self.records_queue = []
        
    def create_table(self):

        data = [['LINE_server', get_current_time(), 'start', 'null']] # init data
        
        self.df = pd.DataFrame(data)
        self.df.columns = self.columns
        #df.show()
    
    def insert_row(self, row):
        row = [[row[0], get_current_time(), row[1], row[2]]]
        self.records_queue.append(row[0])
        rows = self.records_queue.copy()
        self.records_queue = []
        newRow = pd.DataFrame(rows)
        newRow.columns = self.columns
        self.df = self.df.append(newRow, ignore_index=True)

    def view(self, n, uid):
        df = self.df[self.df['UserID'] == uid]
        df = df[['Time', 'Service', 'Message']]
        select_df = df[-n:].T 
        if select_df.to_json() == '{}':
            return 'No records.'
        else:
            return select_df.to_json()
    
    def clean(self, uid):
        self.df = self.df[self.df['UserID'] != uid]
    

