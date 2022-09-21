# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class StackPipeline:

    def __init__(self):
        self.count=1
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='python'
        )
        self.curr = self.conn.cursor()
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS stackoverflow_db""")
        self.curr.execute("""CREATE TABLE stackoverflow_db (   
                                id int NOT NULL AUTO_INCREMENT,                           
                                title VARCHAR(254),                                
                                amount_answers varchar(100),
                                link text,
                                tags text,
                                `time` date,
                                count_visualizations text ,
                                votes text,                                
                                primary key(id)                                                            
                               ) """)


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):

        for questions, time in zip(item['questions'],  item['questionTime']):
            self.curr.execute("""INSERT ignore INTO stackoverflow_db(title,amount_answers,link,tags,`time`,count_visualizations,votes) values (%s,%s,%s,%s,%s,%s,%s)""", (
                questions,
                item['answersNumber'],
                item['links'],
                item['tags'],
                time,
                item['views'],
                item['votes']
            ))

        self.conn.commit()



