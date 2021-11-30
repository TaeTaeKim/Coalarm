
CREATE TABLE IF NOT EXISTS `Corona_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `continent` VARCHAR(20) NOT NULL,
    `total_cases` INT NOT NULL,
    `new_cases` INT NOT NULL,
    `total_deaths` INT NOT NULL,
    `new_deaths` INT NOT NULL,
    `total_recovered` INT NOT NULL,
    `new_recovered` INT NOT NULL,
    `recovered_ratio` FLOAT NOT NULL,
    `critical_ratio` FLOAT NOT NULL,
    `total_caeses_per_1million_population` FLOAT NOT NULL);


CREATE TABLE IF NOT EXISTS `Api_Data` (
    `country` VARCHAR(50) NOT NULL,
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `country_kr` VARCHAR(30) NOT NULL,
    `caution` INT NOT NULL,
    `notice` TEXT NOT NULL);


CREATE TABLE IF NOT EXISTS `Corona_Vaccine_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(30) NOT NULL,
    `vaccinated` FLOAT NOT NULL,
    `fully_vaccinated` FLOAT NOT NULL);


CREATE TABLE IF NOT EXISTS `Exchange_Data` (
    `cur_nm` VARCHAR(50) NOT NULL PRIMARY KEY,
    `cur_unit` VARCHAR(10) NOT NULL,
    `deal_bas_r` VARCHAR(10) NOT NULL);

CREATE TABLE IF NOT EXISTS `Embassy_Data` (
    `iso_code` VARCHAR(10) NOT NULL,
    `embassy_kor_nm` VARCHAR(50) NOT NULL PRIMARY KEY,
    `url` VARCHAR(100) NOT NULL);

CREATE TABLE IF NOT EXISTS `Safety_Data` (
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `safety_index` FLOAT,
    `numbeo_index` FLOAT,
    `homicide_rate` FLOAT,
    `last_terrorism` FLOAT,
    `previous_terrorism` FLOAT);

CREATE TABLE IF NOT EXISTS `Comment` (
    `idx` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `parent` INT NOT NULL,
    `text` VARCHAR(100) NOT NULL,
    `nickname` VARCHAR(30) NOT NULL,
    `write_time` VARCHAR(30) NOT NULL,
    `password` VARCHAR(30) NOT NULL,
    `class` VARCHAR(3) NOT NULL);

CREATE TABLE IF NOT EXISTS `Safety_Score` (
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `country_kr` VARCHAR(30) NOT NULL,
    `score` FLOAT NOT NULL);

