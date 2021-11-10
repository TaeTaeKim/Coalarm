CREATE TABLE country(
    id INT NOT NULL AUTO_INCREMENT,
    isocode VARCHAR(10) NOT NULL,
    countryName VARCHAR(50) NOT NULL,
    caution_lvl INT(1) NOT NULL
    PRIMARY KEY(id)
);

CREATE TABLE notice(
    id INT NOT NULL AUTO_INCREMENT,
    isocode VARCHAR(10) NOT NULL,
    notice TEXT NOT NULL

    PRIMARY KEY(id)
    FOREIGN KEY(isocode) REFERENCES country(isocode) ON UPDATE CASCADE
);