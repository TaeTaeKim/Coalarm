CREATE TABLE IF NOT EXISTS `Corona_Data` (
    `country` VARCHAR(50) NOT NULL,
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `total_cases` INT NOT NULL,
    `new_cases` INT NOT NULL,
    `total_deaths` INT NOT NULL,
    `new_deaths` INT NOT NULL,
    `total_recovered` INT NOT NULL,
    `new_recovered` INT NOT NULL,
    `recovered_ratio` DECIMAL(5,2) NOT NULL,
    `critical` DECIMAL(5,2) NOT NULL,
    `total_caeses_per_1million_population` DECIMAL(5,2) NOT NULL,
    `population` INT NOT NULL);

CREATE TABLE IF NOT EXISTS `Api_Data` (
    `country` VARCHAR(50) NOT NULL,
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `caution` INT NOT NULL,
    `notice` TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS `Corona_Vaccine_Data` (
    `country` VARCHAR(50) NOT NULL,
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `vaccinated` DECIMAL(5,2) NOT NULL,
    `fully_vaccinated` DECIMAL(5,2) NOT NULL);