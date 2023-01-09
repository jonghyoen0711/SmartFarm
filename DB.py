import pymysql
class Database():
    def __init__(self):
        self.db=pymysql.connect(host='localhost',port=3306,user='jh',passwd='1234',db='test',charset='utf8')
        self.cursor = self.db.cursor()
    
    def show(self):
        sql="""SELECT * from sensor """
        
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return(result);
    
    def insert(self,date,hum,temper):
        sql ="""insert into sensor values (%s, %s, %s)"""
        self.cursor.execute(sql,(date,hum,temper))
        self.db.commit()

if __name__ == "__main__":
    db=Database();
    db.show();
