-- 추가 : 대륙 이름 : "continent"
CREATE TABLE IF NOT EXISTS `Corona_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `total_cases` INT NOT NULL,
    `new_cases` INT NOT NULL,
    `total_deaths` INT NOT NULL,
    `new_deaths` INT NOT NULL,
    `total_recovered` INT NOT NULL,
    `new_recovered` INT NOT NULL,
    `recovered_ratio` DECIMAL(5,2) NOT NULL,
    `critical` DECIMAL(5,2) NOT NULL,
    `total_caeses_per_1million_population` FLOAT NOT NULL);
-- 추가 : 나라 한글 이름 : "country_kr"
CREATE TABLE IF NOT EXISTS `Api_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `country_kr` VARCHAR(30) NOT NULL,
    `caution` INT NOT NULL,
    `notice` TEXT NOT NULL);
-- 추가 : 대륙 이름 : "continent"
CREATE TABLE IF NOT EXISTS `Corona_Vaccine_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `vaccinated` DECIMAL(5,2) NOT NULL,
    `fully_vaccinated` DECIMAL(5,2) NOT NULL);