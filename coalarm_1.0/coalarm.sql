
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
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `country_kr` VARCHAR(30) NOT NULL,
    `caution` INT NOT NULL,
    `notice` TEXT NOT NULL);


CREATE TABLE IF NOT EXISTS `Corona_Vaccine_Data` (
    `country` VARCHAR(50) NOT NULL PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `vaccinated` FLOAT NOT NULL,
    `fully_vaccinated` FLOAT NOT NULL);


CREATE TABLE IF NOT EXISTS `Exchange_Data` (
    `cur_nm` VARCHAR(50) NOT NULL PRIMARY KEY,
    `cur_unit` VARCHAR(10) NOT NULL,
    `deal_bas_r` VARCHAR(10) NOT NULL);

CREATE TABLE IF NOT EXISTS `Embassy_Data` (
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `embassy_kor_nm` VARCHAR(50) NOT NULL,
    `url` VARCHAR(100) NOT NULL);

CREATE TABLE IF NOT EXISTS `Safety_Data` (
    `country` VARCHAR(50) NOT NULL,
    `iso_code` VARCHAR(10) NOT NULL PRIMARY KEY,
    `safety_index` FLOAT,
    `numbeo_index` FLOAT,
    `homicide_rate` FLOAT,
    `last_terrorism` FLOAT,
    `previous_terrorism` FLOAT);
)

CREATE TABLE IF NOT EXISTS `Comment` (
    `index` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `iso_code` VARCHAR(10) NOT NULL,
    `class` INT NOT NULL,
    `order` INT NOT NULL,
    `group_num` INT NOT NULL,
    `text` TEXT NOT NULL);
)