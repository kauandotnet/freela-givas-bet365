login_credenciais = {
    'URL_LANGUAGE':'https://www.bet365.com/br/',
    'URL_LOGIN':'https://www.bet365.com/',
	"USER_LOGIN": 'rodrigoreisf', 
    "SENHA_LOGIN": 'OverUnreal34$'
}

urls = {
	"URL_EXTRA_RESULT": "https://extra.bet365.com/results",
    'URL_JSON_BASE_COMPETICOES':'https://extra.bet365.com/ResultsApi/GetCompetitions?sportId={}&fromDate={}&toDate={}',
    'URL_JSON_BASE_FIXTURE':'https://extra.bet365.com/ResultsApi/GetFixtures?sportId={}&competitionId={}&challengeId={}&fixtureId={}&fromDate={}&toDate={}&isDynamic={}&linkId={}&teamId={}&sportDescriptor={}',
    'URL_JSON_BASE_PARTIDA':'https://extra.bet365.com/ResultsApi/GetResults?sportName=sport&sportId={}&fixtureId={}&competitionId={}&fromDate={}&toDate={}&challengeId={}&marketOverride='
}

configParams = {
    'DOMAIN':'BET365_VIRTUAL',
    'SITE_DOMAIN':'https://www.bet365.com/',
    'EXECUTAR_MODO_HEADLESS': True,
    'INTEGRACAO_EXTERNA_HABILITADA':True,
    
    'EXECUCAO_DIARIA': True, #True ou False
    'PROCESSA_POR_PERIODO': None, #[(1, 12, 2019), (10, 12, 2019)] // se [] irá processar os ultimos 6 meses até o dia atual 
    'PROCESSA_ID_COMPETITION':(20120650, 'Copa do Mundo', 'Campeonato do Mundo'), #None ou (20120650, 'Copa do Mundo') 
	
    'INTERVALO_TEMPO':1, #segundos
    'INTERVALO_TEMPO_COMPETICOES':1, #segundos
    'LIMITE_COLETA_COMPETICAO':10, #unidade
    'LIMITE_COLETA_FIXTURE':99999, #unidade

    'DATA_SPORT_ID':'146', 
    'DATA_SPORT_DESCRIPTOR':'FutebolVirtual'
}

html_xpaths = {
    'LOGIN_BOX_USER':'//div[@class="hm-Login "]//div[contains(@class,"UserName")]//input',
    'LOGIN_BOX_PASS':'//div[@class="hm-Login "]//div[contains(@class,"Password")]//input[@class="hm-Login_InputField "]',
    'LOGIN_BTN_OK':'//div[@class="hm-Login "]//button[@class="hm-Login_LoginBtn "]',
    'MODAL_MSG_LOGIN':'//div[contains(@class, "PushTargetedMessageOverlay")]//div[contains(@class, "CloseButton")]',
    'LOGOUT_MENU':'//div[@class ="hm-MembersInfoButton_AccountIcon "]',
    'LOGOUT_LNK_SAIR':'//div[@class="hm-MembersInfoGeneral_Link hm-MembersInfoGeneral_LoggedInLogOut "]',
    'RESULT_BTN_ENCONTRAR':'//div[@class="home-page__search-button"]',
    'RESULT_MODAL_ESPORTE':'//div[@class="results-modal__sports-name"][text()="Futebol Virtual"]',
    'STATUS_CODE_UNAUTH':'//div[@id="content"]//h2'
}


