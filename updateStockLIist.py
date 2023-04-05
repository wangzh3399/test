from basicfunc import *
import akshare as ak




def fullUpdateLocal(dbCursor):
    #从基础的txt更新一次，后面再定期扫描。 这里还有个问题，股票名称还没有获取到，先使用id吧，后面再加
    stocklist = open('./stocklist.txt','r')
    for stock in stocklist:
        insertCmd = 'insert into wxcloudrun_stockstaticdata (stockcode,stockName) VALUE ("'+stock+'","");'
        dbCursor.execute(insertCmd)
def UpdateOnline(dbCursor):
    stockinfoDf = ak.stock_info_a_code_name()
    #stockinfoDf_sz = ak.stock_info_sz_name_code()
    print(stockinfoDf)
    '''
        code   name                                                                                                                                                                                                                                             
0     000001   平安银行
1     000002  万  科Ａ
2     000004   ST国华
3     000005   ST星源
4     000006   深振业Ａ
...      ...    ...
5129  873169   七丰精工
5130  873223   荣亿精密
5131  873305   九菱科技
5132  873339   恒太照明
5133  873527    夜光明
    '''  
    for i in range(0,len(stockinfoDf.index)):
        stockCode = stockinfoDf['code'][i]
        stockName = stockinfoDf['name'][i]
        insertCmd = 'insert into wxcloudrun_stockstaticdata (stockcode,stockName) VALUE ("'+stockCode+'","'+stockName+'");'
        try:
            dbCursor.execute(insertCmd)
        except:
            continue
        print("insert"+stockCode+stockName)

def updateStockListPerDay():
    #每天凌晨更新股票列表，写数据库。退市的保留，只增不删。 启动时判断，如果股票静态信息表如果为空则默认写一次，否则不写。
    dbConn = getDBConn()
    if  dbConn == None:
        exit(0)
    dbCursor = dbConn.cursor()
    '''
    selectStockCmd = 'select stockcode from wxcloudrun_stockstaticdata';
    dbCursor = dbConn.cursor()
    dbCursor.exec(selectStockCmd)
    selectRes = dbCursor.fetchall()
    
    if selectRes == None:
        fullUpdateLocal(dbCursor)
        dbConn.commit()
        dbConn.close()
    '''
    UpdateOnline(dbCursor)
    dbConn.commit()
    dbConn.close()

if __name__ == '__main__':
    updateStockListPerDay()