CREATE TABLE country(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    isocode VARCHAR(10) NOT NULL,
    countryName VARCHAR(50) NOT NULL,
    caution_lvl INT(1) NOT NULL
);

CREATE TABLE notice(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    country_isocode VARCHAR(10) NOT NULL,
    notice TEXT NOT NULL,
    FOREIGN KEY(country_isocode) REFERENCES country(isocode) 
    ON UPDATE CASCADE ON DELETE CASCADE
);