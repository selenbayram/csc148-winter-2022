"""CSC148 Assignment 0: Sample tests

=== CSC148 Winter 2022 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests! Add your own tests
to be confident that your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) University of Toronto
"""
from datetime import date
from io import StringIO
from elections import Election, Jurisdiction

# A string representing one election result.
# StringIO will take the string below and make an object that we can pass to
# method read_results just like we would pass an open file to it.
# We use this in our testing below. You can use it in your own testing, but
# you do not have to.
SHORT_FILE_CONTENTS = 'header\n' + \
                      ','.join(['35090', '"St. Paul\'s"', '"St. Paul\'s"',
                                '" 1"', '"Toronto"', 'N', 'N', '""', '1',
                                '367', '"Bennett"', '""', '"Carolyn"',
                                '"Liberal"', '"Liberal"', 'Y', 'Y', '113'])


def simple_election_setup() -> Election:
    """Set up a simple Election with two ridings and three parties"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1234)
    e.update_results('r1', 'lib', 1345)
    e.update_results('r1', 'pc', 1456)

    e.update_results('r2', 'ndp', 300)
    e.update_results('r2', 'lib', 200)
    e.update_results('r2', 'pc', 100)

    return e


def simple_jurisdiction_setup() -> Jurisdiction:
    """Set up a simple Jurisdiction with a single Election and one result."""
    j = Jurisdiction('Canada')
    res1 = StringIO(SHORT_FILE_CONTENTS)
    j.read_results(2000, 1, 2, res1)
    return j


def test_simple_election_ridings_recorded() -> None:
    """Test Election.ridings_recorded with a simple Election."""
    e = simple_election_setup()
    assert e.ridings_recorded() == ['r1', 'r2']


def test_simple_election_results_for() -> None:
    """Test Election.results_for with a simple Election."""
    e = simple_election_setup()
    assert e.results_for('r1', 'ndp') == 1234


def test_simple_election_riding_winners() -> None:
    """Test Election.riding_winners with a simple Election."""
    e = simple_election_setup()
    assert e.riding_winners('r1') == ['pc']


def test_simple_election_popular_vote() -> None:
    """Test Election.popular_vote with a simple Election."""
    e = simple_election_setup()
    assert e.popular_vote() == {'ndp': 1534, 'lib': 1545, 'pc': 1556}


def test_simple_election_party_seats() -> None:
    """Test Election.party_seats with a simple Election."""
    e = simple_election_setup()
    assert e.party_seats() == {'ndp': 1, 'lib': 0, 'pc': 1}


def test_one_party_one_riding_read_results() -> None:
    """Test Election.read_results with a file with a single line."""
    file = StringIO(SHORT_FILE_CONTENTS)
    e = Election(date(2012, 10, 30))
    e.read_results(file)
    assert e.popular_vote() == {'Liberal': 113}


def test_simple_jurisdiction_party_wins() -> None:
    """Test Jurisdiction.party_wins with a file with a single line. """
    j = simple_jurisdiction_setup()
    assert j.party_wins('Liberal') == [date(2000, 1, 2)]


def test_simple_jurisdiction_party_history() -> None:
    """Test Jurisdiction.party_history with a file with a single line."""
    j = simple_jurisdiction_setup()
    assert j.party_history('Liberal') == {date(2000, 1, 2): 1.0}


def test_simple_jurisdiction_riding_changes() -> None:
    """Test Jurisdiction.riding_changes with two Elections."""
    j = simple_jurisdiction_setup()
    res2 = open('data/toronto-stpauls.csv')
    j.read_results(2004, 5, 15, res2)
    res2.close()
    assert j.riding_changes() == [({"St. Paul's"}, {"Toronto--St. Paul's"})]


def test_jurisdiction_read_results() -> None:
    """Test Jurisdiction.read_results with a sample file."""
    j = simple_jurisdiction_setup()
    f = open('data/easy_data_sample')
    j.read_results(2000, 1, 2, f)
    f.close()
    assert j.party_history("Liberal") == {date(2000, 1, 2): 0.5459401709401709}


def test_jur_riding_changes_with_3_election_dates() -> None:
    j = simple_jurisdiction_setup()
    f = open('data/easy_data_sample')
    j.read_results(2000, 1, 3, f)
    f.close()
    f2 = open('data/data_for_a0')
    j.read_results(2000, 2, 2, f2)
    f2.close()
    assert j.riding_changes() == [(set(), {"Brampton Centre", "Labrador",
                                           "Medicine Hat--Cardston--Warner",
                                           "Parkdale--High Park"}),
                                  ({"Brampton Centre", "Labrador",
                                    "Parkdale--High Park", "St. Paul's"},
                                   {"Toronto--St. Paul's",
                                    "University--Rosedale"})]


if __name__ == '__main__':
    import pytest
    pytest.main(['a0_sample_test.py'])


