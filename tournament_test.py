# Test cases for tournament.py
from tournament import *


# Test creating a new tournament
def testStartTourney():
    # Delete all of the tourneys
    deleteTourneys()
    # Create a new one
    startTourney("World Cup")
    # See if it exists
    c = countTourneys()
    if c != 1:
        raise ValueError(
            "After one tourney start, countTourneys() should be 1.")
    print "\nTEST TOURNEY CREATION: After starting a tourney,"\
          "countTourneys() returns 1.\n"


def testDeleteMatches(tourney):
    deleteMatches(tourney)
    print "1. Matches in a tourney can be deleted"


def testDelete(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    print "2. Player records in a tourney can be deleted."


def testCount(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    c = countPlayers(tourney)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    registerPlayer("Chandra Nalaar", tourney)
    c = countPlayers(tourney)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player in a tourney, "\
          "countPlayers() returns 1."


def testRegisterCountDelete(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    registerPlayer("Markov Chaney", tourney)
    registerPlayer("Joe Malik", tourney)
    registerPlayer("Mao Tsu-hsi", tourney)
    registerPlayer("Atlanta Hope", tourney)
    c = countPlayers(tourney)
    if c != 4:
        raise ValueError(
            "After registering four players in a tourney, "
            "countPlayers should be 4.")
    deletePlayers(tourney)
    c = countPlayers(tourney)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted in a tourney."


def testStandingsBeforeMatches(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    registerPlayer("Melpomene Murray", tourney)
    registerPlayer("Randy Schwartz", tourney)
    standings = playerStandings(tourney)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings "
                         "even before they have played any matches "
                         " a tourney.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in "
                         "tourney's standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players in a tourney should have no "
            "matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches "
                         "played in a tourney.")
    print "6. Newly registered players in a tourney appear in the "\
          "standings with no matches."


def testReportMatches(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    registerPlayer("Bruno Walton", tourney)
    registerPlayer("Boots O'Neal", tourney)
    registerPlayer("Cathy Burton", tourney)
    registerPlayer("Diane Grant", tourney)
    standings = playerStandings(tourney)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tourney)
    reportMatch(id3, id4, tourney)
    standings = playerStandings(tourney)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match "
                             "recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win "
                             "recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins "
                             "recorded.")
    print "7. After a match, players have updated standings in a tourney."


def testPairings(tourney):
    deleteMatches(tourney)
    deletePlayers(tourney)
    registerPlayer("Twilight Sparkle", tourney)
    registerPlayer("Fluttershy", tourney)
    registerPlayer("Applejack", tourney)
    registerPlayer("Pinkie Pie", tourney)
    standings = playerStandings(tourney)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tourney)
    reportMatch(id3, id4, tourney)
    pairings = swissPairings(tourney)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired in a tourney."


if __name__ == '__main__':
    print "\n----------------------------------------------------------\n"
    # Test tourney creation
    testStartTourney()
    print "\n----------------------------------------------------------\n"
    # Delete all tourneys to prepare for other tests
    deleteTourneys()

    tourneys = ["World Cup", "French Open", "World Series"]
    n = 0

    ''' Iterate through a set of tests
        for each tourney while player and match
        data persists in the database from the previous
        tourney.
    '''

    for tourney in tourneys:
        n += 1
        print "#### Pass %d - %s" % (n, tourney)
        startTourney(tourney)
        id = getTourneyIdByName(tourney)
        testDeleteMatches(id)
        testDelete(id)
        testCount(id)
        testRegister(id)
        testRegisterCountDelete(id)
        testStandingsBeforeMatches(id)
        testReportMatches(id)
        testPairings(id)
        print "Success!  All tests pass for - %s -" % (tourney)

    print "\n----------------------------------------------------------\n"
    print "Players and matches were tracked separately "\
          "for the three test tourneys!"
    print "\n----------------------------------------------------------\n"
