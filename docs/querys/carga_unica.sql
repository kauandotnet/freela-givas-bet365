INSERT INTO `bet365`.`sport` (`idSport`,`name`) VALUES (1, 'Futebol Virtual');
INSERT INTO `bet365`.`sport` (`idSport`,`name`) VALUES (2, 'Futebol');

INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (1, 'Vencedor do Jogo', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (2, 'Número de Gols', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (3, 'Resultado Correto', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (4, 'Time a Marcar Primeiro', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (5, 'Intervalo - Resultado Correto', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (6, 'Total de Gols', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (7, 'Para Ambos os Times Marcarem', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (8, 'Para o Time Da Casa Marcar', 1);
INSERT INTO `bet365`.`market` (`idMarket`, `name`, `idSport`) VALUES (9, 'Para o Time  Visitante Marcar', 1);

INSERT INTO `bet365`.`competition` (`idCompetition`, `description`, `alternativeDescription`, `idSport`) VALUES (20120650, 'Copa do Mundo', 'Campeonato do Mundo', 1);
INSERT INTO `bet365`.`competition` (`idCompetition`, `description`, `alternativeDescription`, `idSport`) VALUES (20120654, 'Superleague', null, 1);
INSERT INTO `bet365`.`competition` (`idCompetition`, `description`, `alternativeDescription`, `idSport`) VALUES (20640325, 'Premiership', null, 1);


INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (1, 'over 0.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (2, 'under 0.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (3, 'over 1.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (4, 'under 1.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (5, 'over 2.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (6, 'under 2.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (7, 'over 3.5', 2);
INSERT INTO `bet365_givas`.`typemarket` (`idTypeMarket`,`label`,`idMarket`) VALUES (8, 'under 3.5', 2);
