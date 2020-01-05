
ALTER TABLE bet365.adversary DROP FOREIGN KEY adversary_ibfk_1; 
UPDATE bet365.adversary SET idSport = 20120650;
ALTER TABLE bet365.adversary CHANGE `idSport` `idCompetition` int(11);
ALTER TABLE bet365.adversary ADD FOREIGN KEY (idCompetition) REFERENCES Competition(idCompetition);

ALTER TABLE bet365.competition ADD COLUMN idSport INT(11) AFTER alternativeDescription;
ALTER TABLE bet365.competition ADD FOREIGN KEY (idSport) REFERENCES Sport(idSport);
UPDATE bet365.competition SET idSport = 1;

ALTER TABLE bet365.MatchData ADD COLUMN halfTimeResult VARCHAR(50) NULL AFTER matchResult;
ALTER TABLE bet365.MatchData ADD COLUMN idAdversaryScoreFirst INT(11) NULL AFTER halfTimeResult;