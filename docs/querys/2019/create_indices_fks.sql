CREATE  UNIQUE INDEX un_idx_matchdata_date ON bet365.matchdata(date, idCompetition);

ALTER TABLE bet365.matchdata ADD FOREIGN KEY (idWinner) REFERENCES Adversary(idAdversary);
ALTER TABLE bet365.matchdata ADD FOREIGN KEY (idAdversary1) REFERENCES Adversary(idAdversary);
ALTER TABLE bet365.matchdata ADD FOREIGN KEY (idAdversary2) REFERENCES Adversary(idAdversary);

ALTER TABLE bet365.adversary MODIFY idCompetition INT(11) NOT NULL;