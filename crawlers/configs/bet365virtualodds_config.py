login_credenciais = {
    'URL_LANGUAGE':'https://www.bet365.com/br/',
    'URL_LOGIN':'https://www.bet365.com/',
	"USER_LOGIN": 'rodrigoreisf', 
	"SENHA_LOGIN": 'OverUnreal34$'
}

urls = {
    'SITE_DOMAIN':'https://www.bet365.com/',
	"URL_EXTRA_RESULT": "",
}

configParams = {
    'DOMAIN':'BET365_VIRTUAL_ODDS',  
    'PROCESSA_ID_COMPETITION': None, #(20120650, 'Copa do Mundo', 'Campeonato do Mundo'),  
}

html_xpaths = {
    'LNK_MENU_ESP_VIRTUAIS':'//div[contains(@class, "wn-Classification ")][contains(text(), "Esportes Virtuais")]',
    'LNK_SUBMENU_FUTEBOL':'//div[@class="vr-VirtualsNavBarButton_Label "][text()="Futebol"]',
    'LNK_LISTA_PARTIDAS':'//div[contains(@class, "vr-VirtualRaceNavBarButton")][{}]',
    'DIV_RACE_INFO':'//div[@class="vr-CouponVirtualsMarketGroupButton_RaceInfo "]',
        'TXT_NOME_PARTIDA_ATIVA':'.//div[@class="vr-CouponVirtualsMarketGroupButton_RaceInfoText "]',
        'TXT_EVENTO_INICIADO':'.//div[contains(@class,"vr-CouponVirtualsMarketGroupButton_RaceOff")][not(contains(@class, "Hidden"))]',
    'LST_COMPETITIONS':'//div[contains(@class, "vr-VirtualRacingMeetingsButton ")]',
    'LST_GRUPO_ODDS':'//div[@class="gll-MarketGroup "]',
        'GRUPO_NOME':'.//div[@class="gll-MarketGroupButton cm-MarketGroupButtonWithStats gll-MarketGroup_Open "]',
        'LST_GRUPO_COLUMNS':'.//div[@class="gll-MarketColumnHeader "]//parent::div[contains(@class, "PWidth")]',
            'COLUMN_HEADER':'.//div[@class="gll-MarketColumnHeader "]',
            'CONTAINER_CELULA':'.//div[contains(@class, "Participant")]',
                'CELULA_TITLE':'.//span[1]',
                'CELULA_VALUE':'.//span[2]'
}


