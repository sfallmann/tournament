''' Swiss-system tournament '''
# Module for working with Postgresql DB
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def startTourney(name):
    """Adds a tourney to the tournament database.

    The database assigns a unique serial id number for the tourney.
    Args:
      name: the tourney's name (MUST be unique).
    """
    # Connect to the db
    db = connect()
    # a Control to allow manipulating the database
    c = db.cursor()
    # Execute the sql command
    c.execute('''
                INSERT INTO tourney
                            (name)
                VALUES     (%s)
              ''', (name,))
    # Makes it persist in the db
    db.commit()
    # Close the connection
    db.close()


def deleteTourneys():
    """Remove the tourneys from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tourney;")
    db.commit()
    db.close()


def getTourneyIdByName(name):
    """Gets the id of the tourney by it's name"""
    db = connect()
    c = db.cursor()
    c.execute("""
                SELECT tourney_id
                FROM   tourney
                WHERE  name = %s;
              """, (name,))
    id = c.fetchone()
    db.commit()
    db.close()
    return id


def countTourneys():
    """Returns the number of tourneys started."""
    db = connect()
    c = db.cursor()
    c.execute("""
                SELECT Count(*)
                FROM   tourney;
              """)
    number = c.fetchone()
    db.close()
    return int(number[0])


def deleteMatches(tourney):
    """Remove all the match records for a tourney from the database."""
    db = connect()
    c = db.cursor()
    c.execute("""
                DELETE FROM matches
                WHERE  matches.tourney_id = %s;
              """, (tourney,))
    db.commit()
    db.close()


def deletePlayers(tourney):
    """Remove all the player records for a tourney from the database."""
    db = connect()
    c = db.cursor()
    c.execute("""
                DELETE FROM players
                WHERE  players.tourney_id = %s;
              """, (tourney,))
    db.commit()
    db.close()


def countPlayers(tourney):
    """Returns the number of players currently registered in a tourney."""
    db = connect()
    c = db.cursor()
    c.execute("""
                SELECT Count(*)
                FROM   players
                WHERE  players.tourney_id = %s;
              """, (tourney,))
    number = c.fetchone()
    db.close()
    return int(number[0])


def registerPlayer(name, tourney):
    """Adds a player to the tournament database for a tourney.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
      tourney: the id of the tourney they are entering
    """
    db = connect()
    c = db.cursor()
    c.execute('''
                INSERT INTO players
                            (name,
                             tourney_id)
                VALUES      (%s,
                             %s)
              ''', (name, tourney,))
    db.commit()
    db.close()


def playerStandings(tourney):
    """Returns a list of the players and their win records, sorted by wins
        for a tourney.
        The first entry in the list should be the player in first place,
        or a player tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    # Gets the players id and name for every player
    # within a given tourney and counts the number of
    # matches the player was in and the player's number
    # of wins.
    c.execute('''
                SELECT player_id,
                       name,
                       Count(winner_id) AS wins,
                       Count(match)     AS total_matches
                FROM   (SELECT *
                        FROM   players
                        WHERE  players.tourney_id = %s) AS tourney_players
                       left join participated
                              ON participant = player_id
                       left join matches
                              ON winner_id = player_id
                GROUP  BY player_id,
                          tourney_players.name;
              ''', (tourney,))
    players = c.fetchall()
    db.commit()
    db.close()
    return players


def reportMatch(winner, loser, tourney):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tourney: the id of the tourney the match took place in
    """
    db = connect()
    c = db.cursor()
    c.execute('''
                INSERT INTO matches
                            (winner_id,
                             loser_id,
                             tourney_id)
                VALUES      (%s,
                             %s,
                             %s)
              ''', (winner, loser, tourney,))
    db.commit()
    db.close()


def swissPairings(tourney):
    """Returns a list of pairs of players for the next round of a match
    within a tourney.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    # Gets the id and name of two players from two
    # subqueries where both players had the same
    # number of wins and that both players
    # are not the same player.
    c.execute('''
                SELECT player1,
                       player1name,
                       player2,
                       player2name
                FROM   (SELECT player_id AS player1,
                               name      AS player1name,
                               wins      AS player1_wins
                        FROM   players,
                               player_summary
                        WHERE  player_id = player
                               AND players.tourney_id = %s) AS summary1,
                       (SELECT player_id AS player2,
                               name      AS player2name,
                               wins      AS player2_wins
                        FROM   players,
                               player_summary
                        WHERE  player_id = player
                               AND players.tourney_id = %s) AS summary2
                WHERE  player1 < player2
                       AND player1_wins = player2_wins;
              ''', (tourney, tourney))
    players = c.fetchall()
    db.commit()
    db.close()
    return players
