-- Create the database
CREATE DATABASE tournament;

-- Create the Player table
CREATE TABLE players (
    player_id serial PRIMARY KEY,
    name text
);

-- Create the Matches table
CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    winner_id int REFERENCES players(player_id),
    loser_id int REFERENCES players(player_id)
);

-- Create the view Participated
-- Returns the player_id of the participant in a match
-- and the match_id of each match the participant played in
CREATE OR REPLACE VIEW participated AS
SELECT match_id AS match,
player_id AS participant
FROM matches, players
WHERE player_id IN (winner_id,loser_id)
GROUP BY match_id, player_id;

-- Create the view Player Summary
-- Returns the player_id of the player, the total matches played in
-- and the total wins
CREATE OR REPLACE VIEW player_summary AS
SELECT participant AS player,
COUNT (match) AS total_matches,
COUNT (winner_id) AS wins
FROM participated
LEFT JOIN matches
ON participant = winner_id
GROUP BY participant;


