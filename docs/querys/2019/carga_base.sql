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

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (9, 'gol 0', 2);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (10, 'gol 1', 2);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (11, 'gol 2', 2);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (12, 'gol 3', 2);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (13, 'gol 4', 2);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (1, 'over 0.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (2, 'under 0.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (3, 'over 1.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (4, 'under 1.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (5, 'over 2.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (6, 'under 2.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (7, 'over 3.5', 6);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (8, 'under 3.5', 6);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (14, 'ambas sim', 7);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (15, 'ambas nao', 7);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (16, '0-0 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (17, '1-1 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (18, '2-2 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (19, '1-0 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (20, '2-0 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (21, '2-1 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (22, '3-0 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (23, '3-1 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (24, '4-0 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (25, '0-1 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (26, '0-2 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (27, '1-2 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (28, '0-3 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (29, '1-3 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (30, '0-4 FT', 3);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (31, '0-0 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (32, '1-1 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (33, '1-0 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (34, '2-0 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (35, '0-1 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (36, '0-2 HT', 5);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (37, 'outro HT', 5);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (44, 'casa marca sim', 8);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (45, 'casa marca nao', 8);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (46, 'visitante marca sim', 9);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (47, 'visitante marca nao', 9);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (38, 'mandante HT', 1);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (39, 'empate HT', 1);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (40, 'visitante HT', 1);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (41, 'mandante FT', 1);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (42, 'empate FT', 1);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (43, 'visitante FT', 1);

INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (48, 'casa marca primeiro sim', 4);
INSERT INTO `bet365`.`typemarket` (`idTypeMarket`,`label`, `idMarket`) VALUES (49, 'casa marca primeiro nao', 4);

