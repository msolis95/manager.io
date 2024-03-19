-- Find a list of all forwards with at least 5 goals and 5 assists
-- recorded ordered by their total goal contribution.
-- STRETCH GOAL
SELECT player_name, goals, assists, goals + assists AS goal_contributions
FROM players NATURAL JOIN outfield_players
WHERE position = 'F' AND goals >= 20 AND assists >= 10
ORDER BY goal_contributions DESC, goals DESC, assists DESC
LIMIT 10;

-- Find a list of pairs of a midfielder and a defender in Spain that are valued
-- at most 80 million Euros in total ordered by total market value
SELECT p1.player_name, p1.market_value, p2.player_name, p2.market_value,
	p1.market_value + p2.market_value AS total_market_value
FROM (SELECT * FROM players NATURAL JOIN clubs) AS p1 JOIN 
	(SELECT * FROM players NATURAL JOIN clubs) AS p2
WHERE p1.club_country = 'Spain' AND p2.club_country = 'Spain'
GROUP BY p1.player_id, p2.player_id
HAVING total_market_value <= 80000000
ORDER BY total_market_value
LIMIT 10;

-- Outputs the player information like player's id, player's name, the club of 
-- the player, the birth date of the player, their nationality, market value, 
-- number of apperances, the position, goals, assists, passing accuracy, the key
-- passes and the interceptions per game. This is all for a given player_name, e.g.
-- Jude Bellingham
SELECT *
FROM players NATURAL JOIN outfield_players
WHERE player_name = 'Jude Bellingham';

-- Outputs the player information like player's id, player's name, the club of 
-- the player, the birth date of the player, their nationality, market value, 
-- number of apperances, saves, clean sheets. This is all for a given goalkeeper name, e.g.
-- Thibaut Courtois
SELECT *
FROM players NATURAL JOIN goalkeepers
WHERE player_name = 'Thibaut Courtois'; 

-- Find a list of players between the ages of 15 and 18
SELECT *, get_age(birth_date) AS age
FROM players
GROUP BY player_id
HAVING age BETWEEN 15 AND 18
ORDER BY age DESC, num_appearances DESC
LIMIT 10;

-- Selects the budget for a manager given a username, e.g msolis.
SELECT budget FROM managers WHERE username = 'msolis';

-- Selects players information where the market value is less than or equal to 500000. 
-- It gives a limit of 5 as output. 
SELECT * FROM players WHERE market_value <= 500000 LIMIT 5;

-- Selects players information like player's id, player's name, club id for which the
-- player plays, their birth date, market vlaue and number of appearances. 
-- Limit of output is 5. 
SELECT player_id, player_name, club_id, birth_date, market_value, num_appearances
FROM players WHERE nationality = 'France' LIMIT 5; 

-- Selects the player information like player's id, player's name and market value
-- for a specific category of player that plays in a position {F, M, D}. Limit of 
-- output is 5. 
SELECT player_id, player_name, market_value
FROM players NATURAL JOIN outfield_players WHERE position = 'M' LIMIT 5;

-- Selects the club_id for a given club_name, e.g Futbol Club Barcelona
SELECT club_id FROM clubs WHERE club_name = 'Futbol Club Barcelona';

-- Gives the maximun player id there is. 
SELECT MAX(player_id) AS max_player_id FROM players;

-- Inserts into players table player_id, player_name, club_id, birth_date, nationality
-- market value and number of appearances. See example below. 
INSERT INTO players
    VALUES (1229925, 'Jeremy de Leon', 131, '2003/02/25', 'Colombia', 5000, 52);

-- Selects the manager_id, manager name, the budget of every manager until limit 5.
-- If the budget is null puts 0. 
SELECT manager_id, manager_name, IFNULL(budget, 0)
FROM managers LIMIT 5;

-- Updates the managers table setting the budget to what the manager wants, e.g. 50000
-- for a given username of the manager, e.g. msolis. 
UPDATE managers
	SET budget = 50000
	WHERE username = 'msolis';

-- Updates the players tablet setting the number of appearances to what the 
-- admin wants e.g. 20 for a given player name e.g. Kylian Mbappe
UPDATE players
	SET num_appearances = 20
	WHERE player_name = 'Kylian Mbappe';