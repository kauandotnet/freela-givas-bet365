ALTER TABLE bet365.matchodds DROP COLUMN yes;
ALTER TABLE bet365.matchodds DROP COLUMN no;

ALTER TABLE bet365.typemarket ADD COLUMN idMarket INT(11) NULL AFTER label;
ALTER TABLE bet365.typemarket ADD FOREIGN KEY (idMarket) REFERENCES market(idMarket);

ALTER TABLE bet365.maxima ADD COLUMN lastSequenceCount INT(11) NOT NULL DEFAULT 0 AFTER broken;