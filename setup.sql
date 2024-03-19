-- CREATE DATABASE manageriodb;
-- USE manageriodb;

-- clean up old tables;
-- must drop tables with foreign keys first
-- due to referential integrity constraints
DROP TABLE IF EXISTS goalkeepers;
DROP TABLE IF EXISTS outfield_players;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS manager_employment;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS managers;

-- Represents strong entity set managers uniquely identified
-- by their ID, 
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
CREATE TABLE managers (
    -- database-generated ID for manager
    manager_id          SMALLINT UNSIGNED AUTO_INCREMENT,
    -- name of the manager
    manager_name        VARCHAR(45)     NOT NULL,
    -- user-chosen username used to log into their account,
    -- up to 20 characters long
    username            VARCHAR(20) UNIQUE NOT NULL,
    -- salt of fixed length 8 for hashing password
    salt                CHAR(8)         NOT NULL,
    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    password_hash       BINARY(64)      NOT NULL,
    -- optional feature for users to make their searching
    -- experiences easier by not going over budget
    budget              NUMERIC(12, 2),
    PRIMARY KEY (manager_id)
);
 
-- Represents strong entity set clubs uniquely identified
-- by their ID
CREATE TABLE clubs (
    -- club ID taken from Kaggle dataset
    club_id             MEDIUMINT UNSIGNED,
    -- soccer club name
    club_name           VARCHAR(60)     NOT NULL,
    -- country where the club is located
    club_country        VARCHAR(20)     NOT NULL,
    PRIMARY KEY (club_id)
);

-- Represents the strong entity relationship "are employed by" between
-- managers and clubs, managers who are not in this table are unemployed
CREATE TABLE manager_employment (
    manager_id          SMALLINT UNSIGNED,
    -- clubs only have one manager
    club_id             MEDIUMINT UNSIGNED UNIQUE,
    PRIMARY KEY (manager_id),
    FOREIGN KEY (manager_id) REFERENCES managers (manager_id),
    FOREIGN KEY (club_id) REFERENCES clubs (club_id)
);

-- Represents strong entity set players uniquely identified
-- by their ID
CREATE TABLE players (
    -- player ID taken from Kaggle dataset
    player_id           MEDIUMINT UNSIGNED,
    -- complete player name
    player_name         VARCHAR(50)         NOT NULL,
    -- club that the player plays for
    club_id             MEDIUMINT UNSIGNED,
    birth_date          DATE                NOT NULL,
    -- nationality of the player, the country they represent
    -- at the international level of competition
    nationality         VARCHAR(25)         NOT NULL,
    -- market value of the player in Euros, less than 250 million
    market_value        NUMERIC(12, 1)      NOT NULL,
    -- statistics of the player, less than 75
    num_appearances     NUMERIC(2)          NOT NULL,
    PRIMARY KEY (player_id),
    FOREIGN KEY (club_id) REFERENCES clubs (club_id)
);

CREATE TABLE outfield_players (
    player_id               MEDIUMINT UNSIGNED,
    -- abbreviated general position of the player
    -- defender, midfielder, or forward
        -- to implement later: specialized positions
        -- 'ST', 'W', 'CM', 'CDM', 'CB', 'LB', 'RB'
    position                ENUM('D', 'M', 'F') NOT NULL,
    -- total number of goals scored in the season, less than 60
    goals                   NUMERIC(2)          NOT NULL,
    -- total number of assists made in the season, less than 40
    assists                 NUMERIC(2)          NOT NULL,
    -- average passing accuracy as a percentage
    passing_accuracy        NUMERIC(5,2)        NOT NULL,
    -- average number of key passes per game, less than 10
    key_passes_per_game     NUMERIC(3,2)        NOT NULL,
    -- average number of key passes per game, less than 10
    interceptions_per_game  NUMERIC(5,2)        NOT NULL,
    PRIMARY KEY (player_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);

CREATE TABLE goalkeepers (
    player_id               MEDIUMINT UNSIGNED,
    -- number of saves made in the season, less than 250
    saves                   TINYINT UNSIGNED    NOT NULL,
    -- number of clean sheets achieved in the season,
    -- less than 25
    clean_sheets            NUMERIC(2)          NOT NULL,
    PRIMARY KEY (player_id),
    FOREIGN KEY (player_id) REFERENCES players (player_id)  
);

CREATE INDEX idx_market_values ON players (market_value);
CREATE INDEX idx_market_values ON outfield_players (goals, assists);
CREATE INDEX idx_market_values ON goalkeepers (saves, clean_sheets);