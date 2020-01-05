
configParams = {   
    'TIMER': 3, #seconds
    'TIMER_ODDS': 10, #seconds
    'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'SAVE_SELENIUM_REQUEST_IMAGE':False
}

cookie = {
    'SESSION_COOKIE':'aps03=ct=28&lng=33; bet365SportsExtra=settings=0,0,0,0,0,16,0,,0,1; state=0; pstk={}'
}

threads = {
    'MAX_COUNT': 1
}

database = {
    'mysql_conn_prod':'mysql+pymysql://root:123456@localhost/bet365_givas',
}
conexao_banco_ativa = { 'mysql_conn': database['mysql_conn_prod']}

