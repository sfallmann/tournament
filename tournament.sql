-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create table players (
    id serial primary key,
    name text
);

create table matches (
    id serial primary key,
    player_one int references players(id),
    player_two int references players(id)
);

create table winners (
    match_id int references matches(id),
    winner_id int references players(id),
);

CREATE VIEW match_summary AS
SELECT matches.id AS match,
player_one AS p1,
player_two AS p2,
winner_id AS winner
FROM matches, winners
WHERE winner_id = player_one
OR winner_id = player_two;


SELECT players.id, players.name,
COUNT(matches.id) AS num_matches,
COUNT(winner_id) AS wins
FROM players
LEFT JOIN match_summary
ON players.id = player_one
OR players.id = player_two;

    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

SELECT match.id FROM matches WHERE (player_one = winner or player_two = winner)
AND (player_one = loser or player_two = loser)


INSERT INTO winners
(match_id, winner_id) VALUES (%s)


