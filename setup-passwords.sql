-- Generates a salt for hashing passwords with a specified
-- number of characters 
DROP FUNCTION IF EXISTS make_salt;
DELIMITER !
CREATE FUNCTION make_salt()
RETURNS CHAR(8) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(8) DEFAULT '';
    -- don't want to generate more than 20 characters of salt
    DECLARE num_chars INT DEFAULT 8;
    -- generate the salt, characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;
    RETURN salt;
END !
DELIMITER ;

-- Authenticates the specified username and password against the data
-- in the user_info table. Returns 1 if the user appears in the table and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DROP FUNCTION IF EXISTS authenticate;
DELIMITER !
CREATE FUNCTION authenticate(username_arg VARCHAR(20), password VARCHAR(20))
    RETURNS BOOLEAN DETERMINISTIC
BEGIN
    RETURN (SELECT COUNT(*)
        FROM managers
        WHERE username = username_arg AND password_hash = SHA2(CONCAT(salt, password), 256));
END !
DELIMITER ;

-- Generates a new salt and changes the user's password to the new given
-- password (after salting and hashing)
DROP PROCEDURE IF EXISTS change_password;
DELIMITER !
CREATE PROCEDURE change_password(username_arg VARCHAR(20), new_password VARCHAR(20))
BEGIN
    DECLARE new_salt CHAR(8) DEFAULT make_salt();
    UPDATE managers
        SET salt = new_salt, password_hash = SHA2(CONCAT(new_salt, new_password), 256)
        WHERE username = username_arg;
END !
DELIMITER ;