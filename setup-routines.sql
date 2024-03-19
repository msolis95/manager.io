
-- Function to get the age of a player based on their birth date
DROP FUNCTION IF EXISTS get_age;
DELIMITER !
CREATE FUNCTION get_age(birth_date DATE) RETURNS NUMERIC(4, 2) DETERMINISTIC
    BEGIN
        RETURN ROUND(DATEDIFF(CURDATE(), birth_date)/365.0, 2);
    END !
DELIMITER ;

-- Procedure for adding a new manager to the managers table
DROP PROCEDURE IF EXISTS insert_manager;
DELIMITER !
CREATE PROCEDURE insert_manager (
        manager_name_arg VARCHAR(45),
        manager_username VARCHAR(20),
        password VARCHAR(20),
        manager_club VARCHAR(50),
        manager_budget NUMERIC(12, 2)
    )
BEGIN
    -- salt used for hashing the password
    DECLARE new_salt CHAR(8) DEFAULT make_salt();
    -- hashed version of password
    DECLARE hashed_password BINARY(64) DEFAULT SHA2(CONCAT(new_salt, password), 256);
    -- creating new row in the managers table
    INSERT INTO managers (manager_name, username, salt, password_hash, budget)
        VALUES (manager_name_arg, manager_username, new_salt, hashed_password, manager_budget);
    IF manager_club IS NOT NULL THEN
        INSERT INTO manager_employment
            VALUES ((SELECT MAX(manager_id) FROM managers),
                    (SELECT club_id
                    FROM clubs
                    WHERE club_name = manager_club));
    END IF;
END !
DELIMITER ;

-- Every time a player's market value is updated, which happens every week or
-- so, the budgets of the old and new clubs can be updated to reflect the
-- DROP TRIGGER IF EXISTS trg_player_updated; -- causes warning for trigger
DELIMITER !
CREATE TRIGGER trg_player_updated AFTER UPDATE
    ON players FOR EACH ROW
BEGIN
    -- if player transferred clubs
    IF NEW.market_value <> OLD.market_value THEN
        -- update old manager's budget
        UPDATE managers
            SET budget = budget + NEW.market_value - OLD.market_value
            WHERE club_id = NEW.club_id;
    END IF;
END !
DELIMITER ;

CALL insert_manager('Mario Solis', 'msolis', 'Pizza25', 'Futbol Club Barcelona', 10000000);
CALL insert_manager('Julian Navarro Rodriguez', 'jnavarro', 'Sushi001', 'Paris Saint-Germain Football Club', 12000000);
CALL insert_manager('Bryan Oliveira', 'boliveir', 'EuropaChamps', 'Sevilla Fútbol Club S.A.D.', NULL);
CALL insert_manager('Camilo Garrido', 'cgarrido', 'aguerooo', 'Manchester City Football Club', 12000000);
CALL insert_manager('Rafael Crespo', 'rcrespo', 'ynwa2024', 'Liverpool Football Club', NULL);