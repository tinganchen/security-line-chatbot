from pyspark.sql import SparkSession
import datetime

def get_current_time():
    return str(datetime.datetime.now())[:19]

class log:
    def __init__(self):
        self.df = None
        self.columns = ['UserID', 'Time', 'Service', 'Message']
        self.spark = SparkSession.builder.getOrCreate()
        self.records_queue = []
        
    def create_table(self):

        data = [('LINE_server', get_current_time(), 'start', 'null')] # init data
        
        self.df = self.spark.createDataFrame(data, self.columns)
    
        #df.show()
    
    def insert_row(self, row):
        row = (row[0], get_current_time(), row[1], row[2])
        self.records_queue.append(row)
        rows = self.records_queue
        self.records_queue = []
        newRow = self.spark.createDataFrame(rows, self.columns)
        self.df = self.df.union(newRow)

    def view(self, n, uid):
        df = self.df.filter(self.df['UserID'] == uid)
        df = df.toPandas()
        df = df[['Time', 'Service', 'Message']]
        select_df = df[-n:].T #df[-n:].T
        if select_df.to_json() == '{}':
            return 'No records.'
        else:
            return select_df.to_json()
    
    def clean(self, uid):
        self.df = self.df.filter(self.df['UserID'] != uid)
    

