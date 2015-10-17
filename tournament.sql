-- Create the database
CREATE DATABASE tournament;

-- Connect to database
\c tournament

-- Naming the table tourney instead of "tournament" to avoid confusion
-- All references will be to tourney throughout to be consistent
CREATE TABLE tourney
  (
     tourney_id SERIAL PRIMARY KEY,
     name       VARCHAR(80) NOT NULL UNIQUE
  );

-- Create the Player table
CREATE TABLE players
  (
     player_id  SERIAL PRIMARY KEY,
     name       VARCHAR(80) NOT NULL,
     tourney_id INT REFERENCES tourney(tourney_id) ON DELETE CASCADE
  );

-- Create the Matches table
CREATE TABLE matches
  (
     match_id   SERIAL PRIMARY KEY,
     winner_id  INT REFERENCES players(player_id) NOT NULL,
     loser_id   INT REFERENCES players(player_id) NOT NULL,
     tourney_id INT REFERENCES tourney(tourney_id) ON DELETE CASCADE
  );

-- Create the view Participated
-- Returns the player_id of the participant in a match
-- and the match_id of each match the participant played in
CREATE OR replace VIEW participated
AS
  SELECT match_id  AS match,
         player_id AS participant
  FROM   matches,
         players
  WHERE  player_id IN ( winner_id, loser_id )
         AND players .tourney_id = matches.tourney_id
  GROUP  BY match_id,
            player_id;

-- Create the view Player Summary
-- Returns the player_id of the player, the total matches played in
-- and the total wins
CREATE OR replace VIEW player_summary
AS
  SELECT participant       AS player,
         Count (match)     AS total_matches,
         Count (winner_id) AS wins
  FROM   participated
         left join matches
                ON participant = winner_id
  GROUP  BY participant;
