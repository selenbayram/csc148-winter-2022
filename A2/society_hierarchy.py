"""Assignment 2: Society Hierarchy (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Sadia Sharmin, Diane Horton, Dina Sabie, Sophia Huynh, and
         Jonathan Calver.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Sadia Sharmin, Diane Horton, Dina Sabie, Sophia Huynh, and
                   Jonathan Calver

=== Module description ===
This module contains all of the classes necessary to model the entities in a
society's hierarchy.

REMINDER: You must NOT use list.sort() or sorted() in your code. Instead, use
the merge() function we provide for you below.
"""
from __future__ import annotations
from typing import List, Optional, TextIO, Any


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Preconditions:
    - <lst1>> is sorted and <lst2> is sorted.
    - All of the elements of <lst1> and <lst2> are of the same type, and they
      are comparable (i.e. their type implements __lt__).

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """

    i1 = 0
    i2 = 0
    new_list = []

    while i1 < len(lst1) and i2 < len(lst2):
        if lst1[i1] < lst2[i2]:
            new_list.append(lst1[i1])
            i1 += 1
        else:
            new_list.append(lst2[i2])
            i2 += 1

    new_list.extend(lst1[i1:])
    new_list.extend(lst2[i2:])

    return new_list


###########################################################################
# Task 1: Citizen and Society
###########################################################################
class Citizen:
    """A Citizen: a citizen in a Society.

    === Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - cid > 0
    - 0 <= rating <= 100
    - self._subordinates is in ascending order by the subordinates' IDs
    - If _superior is a Citizen, this Citizen is part of its _subordinates list
    - Each Citizen in _subordinates has this Citizen as its _superior
    """
    cid: int
    manufacturer: str
    model_year: int
    job: str
    rating: int
    _superior: Optional[Citizen]
    _subordinates: List[Citizen]

    def __init__(self, cid: int, name: str, model_year: int,
                 job: str, rating: int) -> None:
        """Initialize this Citizen with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, and rating <rating>.

        A Citizen initially has no superior and no subordinates.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c1.cid
        1
        >>> c1.rating
        50
        """
        self.cid = cid
        self.manufacturer = name
        self.model_year = model_year
        self.job = job
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Any) -> bool:
        """Return True if <other> is a Citizen and this Citizen's cid is less
        than <other>'s cid.

        If other is not a Citizen, raise a TypeError.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3042, "Manager", 30)
        >>> c1 < c2
        True
        """
        if not isinstance(other, Citizen):
            raise TypeError

        return self.cid < other.cid

    def __str__(self) -> str:
        """Return a string representation of the tree rooted at this Citizen.
        """
        return self._str_indented().strip()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        me = f'{str(self.cid)} (rating = {self.rating})'
        if isinstance(self, DistrictLeader):
            me += f' --> District Leader for {self._district_name}'
        s = '  ' * depth + me + '\n'
        for subordinate in self.get_direct_subordinates():
            # Note that the ‘depth’ argument to the recursive call is
            # modified.
            s += subordinate._str_indented(depth + 1)
        return s

    def get_superior(self) -> Optional[Citizen]:
        """Return the superior of this Citizen or None if no superior exists.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c1.get_superior() is None
        True
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_superior().cid
        2
        """
        return self._superior

    def set_superior(self, new_superior: Optional[Citizen]) -> None:
        """Update the superior of this Citizen to <new_superior>

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.set_superior(c2)
        >>> c1.get_superior().cid
        2
        """
        self._superior = new_superior

    def get_direct_subordinates(self) -> List[Citizen]:
        """Return a new list containing the direct subordinates of this Citizen.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_direct_subordinates()[0].cid
        2
        """
        return self._subordinates[:]

    ###########################################################################
    # While not called by the client code, these methods may be helpful to
    # you and will be tested. You can (and should) call them in the other
    # methods that you implement when appropriate.
    ###########################################################################

    def add_subordinate(self, subordinate: Citizen) -> None:
        """Add <subordinate> to this Citizen's list of direct subordinates,
        keeping the list of subordinates in ascending order by their ID.

        Update the new subordinate's superior to be this Citizen.

        Precondition: The given <subordinate> has no existing superior.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c2.add_subordinate(c1)
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c1.get_superior() is c2
        True
        """
        subs = self.get_direct_subordinates()
        lst = merge(subs, [subordinate])
        self._subordinates = lst
        subordinate.set_superior(self)
        return None

    def remove_subordinate(self, cid: int) -> None:
        """Remove the subordinate with the ID <cid> from this Citizen's list
        of subordinates.

        Furthermore, remove that (former) subordinate from the hierarchy by
        setting its superior to None.

        Precondition: This Citizen has a subordinate with ID <cid>.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c2.remove_subordinate(1)
        >>> c2.get_direct_subordinates()
        []
        >>> c1.get_superior() is None
        True
        """

        for sub in self._subordinates:  # loop through subordinates
            if sub.cid == cid:
                self._subordinates.remove(sub)  # remove
                sub._superior = None  # set superior as None
        return None

    def become_subordinate_to(self, superior: Optional[Citizen]) -> None:
        """Make this Citizen a direct subordinate of <superior>.

        If this Citizen already had a superior, remove this Citizen from the
        old superior's list of subordinates.

        If <superior> is None, just set this Citizen's superior to None.

        Precondition:
        - the given <subordinate> has no existing superior

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_superior().cid
        2
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c1.become_subordinate_to(None)
        >>> c1.get_superior() is None
        True
        >>> c2.get_direct_subordinates()
        []
        """

        if self._superior is not None:  # if there is old superior
            self._superior.remove_subordinate(self.cid)  # remove from old

        self._superior = superior

        if superior is not None:
            superior.add_subordinate(self)

    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Check this Citizen and its subordinates to find and return the
        Citizen that has the ID <cid>.

        If neither this Citizen nor any of its subordinates (both direct and
        indirect) have the ID <cid>, return None.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_citizen(1) is c1
        True
        >>> c2.get_citizen(3) is None
        True
        """
        # Note: This method must call itself recursively
        if self.cid == cid:
            return self

        else:  # check subordinate!!
            for subordinate in self._subordinates:
                if subordinate.get_citizen(cid) is not None:
                    return subordinate.get_citizen(cid)
        return None

    ###########################################################################
    # Task 1.2
    ###########################################################################

    def get_all_subordinates(self) -> List[Citizen]:
        """Return a new list of all of the subordinates of this Citizen in
        order of ascending IDs.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "S.T.A.R. Lab", 3040, "Commander", 10)
        >>> c10 = Citizen(10, "S.T.A.R. Lab", 3041, "Commander", 20)
        >>> c11 = Citizen(11, "S.T.A.R. Lab", 3042, "Commander", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c10.become_subordinate_to(c4)
        >>> c11.become_subordinate_to(c4)
        >>> c3.get_all_subordinates()[0].cid
        1
        >>> c3.get_all_subordinates()[1].cid
        2
        >>> c3.get_all_subordinates()[2].cid
        4
        >>> len(c3.get_all_subordinates()) == 5
        True
        >>> c3.get_all_subordinates()[3].cid
        10
        >>> c3.get_all_subordinates()[4].cid
        11
        >>> cc1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> cc1.get_all_subordinates()
        []
        """
        # Note: This method must call itself recursively

        lst = self.get_direct_subordinates()  # add the direct ones first

        for subordinate in self._subordinates:  # now look through the directs
            lst = merge(subordinate.get_all_subordinates(), lst)

        return lst

    # Hints:
        # - Recall that each Citizen's subordinates list is sorted in ascending
        #   order.
        # - Use the merge helper function.

    def get_society_head(self) -> Citizen:
        """Return the head of the Society (i.e. the top-most superior Citizen,
        a.k.a. the root of the hierarchy).

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "S.T.A.R. Lab", 3040, "Commander", 10)
        >>> c10 = Citizen(10, "S.T.A.R. Lab", 3041, "Commander", 20)
        >>> c11 = Citizen(11, "S.T.A.R. Lab", 3042, "Commander", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c10.become_subordinate_to(c4)
        >>> c11.become_subordinate_to(c4)
        >>> c1.get_society_head().cid
        3
        >>> cc1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> cc1.get_society_head().cid
        1
        """
        # Note: This method must call itself recursively
        # the head of the society is the citizen with no superiors

        if self.get_superior() is None:
            return self
        else:
            return self._superior.get_society_head()

    def get_closest_common_superior(self, cid: int) -> Citizen:
        """Return the closest common superior that this Citizen and the
        Citizen with ID <cid> share.

        If this Citizen is the superior of <cid>, return this Citizen.

        Precondition: A citizen with the given <cid> exists in this hierarchy.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c10 = Citizen(10, "Hookins National Lab", 3033, "Engineer", 90)
        >>> c6 = Citizen(6, "Hookins National Lab", 3033, "Engineer", 90)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c10.become_subordinate_to(c2)
        >>> c6.become_subordinate_to(c10)
        >>> c3.get_closest_common_superior(1) == c3
        True
        >>> c3.get_closest_common_superior(3) == c3
        True
        >>> c1.get_closest_common_superior(5) == c3
        True
        >>> c1.get_closest_common_superior(10) == c2
        True
        >>> c6.get_closest_common_superior(1) == c2
        True
        >>> c6.get_closest_common_superior(5) == c3
        True
        >>> c6.get_closest_common_superior(4) == c3
        True
        >>> c6.get_closest_common_superior(2) == c2
        True
        """
        # Note: This method must call itself recursively

        # get_all_subordinates -> Return a new list of all the subordinates
        # of this Citizen in order of ascending IDs

        # get_citizen -> Check this Citizen and its subordinates to find and
        # return the Citizen that has the ID <cid>.
        # If neither this Citizen nor any of its subordinates (both direct and
        # indirect) have the ID <cid>, return None.

        if self.get_citizen(cid) or self.cid == cid:
            return self

        # if cid is not in this citizen's subordinates, check if it is in sup
        else:
            value = self._superior.get_closest_common_superior(cid)
        return value

    def _return_superiors(self) -> List[Citizen]:
        """Return a list of all superiors of this citizen in order from closest
        to furthest.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c6 = Citizen(6, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c6.become_subordinate_to(c5)
        >>> c6._return_superiors()[0].cid
        5
        >>> c6._return_superiors()[1].cid
        4
        >>> c6._return_superiors()[2].cid
        3
        >>> c1._return_superiors()[0].cid
        2
        >>> c1._return_superiors()[1].cid
        3
        """

        if self.get_superior() != self.get_society_head():  # if not at head
            lst = [self.get_superior()]  # do stuff to it
            if self._superior._return_superiors():
                lst.extend(self._superior._return_superiors())
        else:  # if at head do nothing
            return []

        lst.append(self.get_society_head())  # now append head at end
        return lst  # return list from closest to furthest superior!

    def _id_to_citizen(self, cid: int) -> Optional[Any]:
        """Return a list of all superiors of this citizen in order from closest
        to furthest

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c6 = Citizen(6, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c6.become_subordinate_to(c5)
        >>> c5._id_to_citizen(5).cid
        5
        >>> c5._id_to_citizen(6).cid
        6
        """

        lst = [self.get_society_head()]
        lst.extend(self.get_society_head().get_all_subordinates())

        for citizen in lst:
            if citizen.cid == cid:
                return citizen
        return None

    ###########################################################################
    # Task 2.2
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the immediate district that the Citizen belongs to (or
        leads).

        If the Citizen is not part of any districts, return an empty string.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.get_district_name()
        ''
        >>> c2.get_district_name()
        'District A'
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_district_name()
        'District A'
        >>> c6 = DistrictLeader(6, "Hookins National Lab", 3024, "Manager", \
        30, "Area 52")
        >>> c5 = DistrictLeader(5, "Hookins National Lab", 3024, "Manager", \
        30, "Finance")
        >>> c9 = Citizen(9, "Starky Industries", 3024, "Labourer", 50)
        >>> c9.get_district_name()
        ''
        >>> c9.become_subordinate_to(c5)
        >>> c9.get_district_name()
        'Finance'
        >>> c5.get_district_name()
        'Finance'
        >>> c5.become_subordinate_to(c6)
        >>> c9.get_district_name()
        'Finance'
        >>> c5.get_district_name()
        'Finance'
        >>> c6.get_district_name()
        'Area 52'
        """
        # Note: This method must call itself recursively

        if self._superior is None:
            return ''

        elif isinstance(self, DistrictLeader):  # if the superior is led
            return self.get_district_name()

        else:
            return self._superior.get_district_name()

    def rename_district(self, district_name: str) -> None:
        """Rename the immediate district which this Citizen is a part of to
        <district_name>.

        If the Citizen is not part of a district, do nothing.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.become_subordinate_to(c2)
        >>> c1.rename_district('District B')
        >>> c1.get_district_name()
        'District B'
        >>> c2.get_district_name()
        'District B'
        >>> c6 = DistrictLeader(6, "Hookins National Lab", 3024, "Manager", \
        30, "Area 52")
        >>> c5 = DistrictLeader(5, "Hookins National Lab", 3024, "Manager", \
        30, "Finance")
        >>> c9 = Citizen(9, "Starky Industries", 3024, "Labourer", 50)
        >>> c9.become_subordinate_to(c5)
        >>> c9.rename_district('Selen')
        >>> c9.get_district_name()
        'Selen'
        >>> c5.get_district_name()
        'Selen'
        >>> c5.become_subordinate_to(c6)
        >>> c5.get_district_name()
        'Selen'
        >>> c5.rename_district('Toronto')
        >>> c9.get_district_name()
        'Toronto'
        >>> c5.get_district_name()
        'Toronto'
        >>> c6.get_district_name()
        'Area 52'
        >>> c6.rename_district('Selin')
        >>> c6.get_district_name()
        'Selin'
        """

        # Note: This method must call itself recursively
        # find district
        # when found, rename it
        if self._superior is None:
            if isinstance(self, DistrictLeader):
                DistrictLeader.rename_district(self, district_name)
            return None

        elif isinstance(self, DistrictLeader):  # if the superior is led
            DistrictLeader.rename_district(self, district_name)
            return None

        else:
            return self._superior.rename_district(district_name)

    ###########################################################################
    # Task 3.2 Helper Method
    ###########################################################################

    def get_highest_rated_subordinate(self) -> Citizen:
        """Return the direct subordinate of this Citizen with the highest
        rating.

        Precondition: This Citizen has at least one subordinate.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", 30,
        ... "District A")
        >>> c3 = DistrictLeader(3, "S.T.A.R.R.Y Lab", 3000, "Commander", 60,
        ... "District X")
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Hookins National Lab'
        >>> c1.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Starky Industries'
        """
        # Hint: This can be used as a helper function for `delete_citizen`
        subs = self.get_direct_subordinates()

        highest = self
        rate = -1
        for sub in subs:
            if sub.rating > rate:
                rate = sub.rating
                highest = sub

        return highest


class Society:
    """A society containing citizens in a hierarchy.

    === Private Attributes ===
    _head:
        The root of the hierarchy, which we call the "head" of the Society.
        If _head is None, this indicates that this Society is empty (there are
        no citizens in this Society).

    === Representation Invariants ===
    - No two Citizens in this Society have the same cid.
    """
    _head: Optional[Citizen]

    def __init__(self, head: Optional[Citizen] = None) -> None:
        """Initialize this Society with the head <head>.

        >>> o = Society()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def __str__(self) -> str:
        """Return a string representation of this Society's tree.

        For each node, its item is printed before any of its descendants'
        items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return str(self._head)

    ###########################################################################
    # You may use the methods below as helper methods if needed.
    ###########################################################################
    def get_head(self) -> Optional[Citizen]:
        """Return the head of this Society.
        """
        return self._head

    def set_head(self, new_head: Citizen) -> None:
        """Set the head of this Society to <new_head>.
        """
        self._head = new_head

    ###########################################################################
    # Task 1.3
    ###########################################################################
    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Return the Citizen in this Society who has the ID <cid>. If no such
        Citizen exists, return None.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024,  "Labourer", 50)
        >>> o.add_citizen(c1)
        >>> o.get_citizen(1) is c1
        True
        >>> o.get_citizen(2) is None
        True
        """
        # Hint: Recall that self._head is a Citizen object, so any of Citizen's
        # methods can be used as a helper method here.
        if self._head is None:
            return None
        return self._head.get_citizen(cid)

    def get_all_citizens(self) -> List[Citizen]:
        """Return a list of all citizens, in order of increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.add_citizen(c6, 2)
        >>> o.add_citizen(c1, 4)
        >>> o.add_citizen(c3, 1)
        >>> o.add_citizen(c5, 1)
        >>> o.get_all_citizens() == [c1, c2, c3, c4, c5, c6]
        True
        """

        lst = merge([self._head], Citizen.get_all_subordinates(self._head))
        return lst

    def add_citizen(self, citizen: Citizen, superior_id: int = None) -> None:
        # CHECK THIS!!!
        """Add <citizen> to this Society as a subordinate of the Citizen with
        ID <superior_id>.

        If no <superior_id> is provided, make <citizen> the new head of this
        Society, with the original head becoming the one and only subordinate
        of <citizen>.

        Preconditions:
        - citizen.get_superior() is None.
        - if <superior_id> is not None, then the Society contains a Citizen with
          ID <superior_id>.
        - Society does not already contain any Citizen with the same ID as
          <citizen>.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Some Lab", 3024, "Lawyer", 30)
        >>> c3 = Citizen(3, "Some Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c2)
        >>> o.get_head() is c2
        True
        >>> o.add_citizen(c1, 2)
        >>> o.get_head() is c2
        True
        >>> o.get_citizen(1) is c1
        True
        >>> c1.get_superior() is c2
        True
        >>> o.add_citizen(c3)
        >>> o.get_head() is c3
        True
        >>> c3.get_all_subordinates() == [c1, c2]
        True
        >>> c2.get_superior() is c3
        True
        >>> c1.get_superior() is c2
        True
        """

        if self.get_head() is None:
            self._head = citizen

        elif superior_id is None:  # have to make the citizen the new head
            # know: there is already a head for this society with potential
            # subordinates
            prev_head = self._head
            self._head = citizen
            prev_head.become_subordinate_to(citizen)

        else:
            # know: self.get_head() is not None and superior_id is not None
            # i.e. there is a head in this society + we are going to make this
            # <citizen> a subordinate of the citizen with id <superior_id>
            lst = self.get_all_citizens()

            for cit in lst:  # check all citizens
                if cit.cid == superior_id:  # if this matches
                    citizen.become_subordinate_to(cit)  # make it subordinate

    def get_citizens_with_job(self, job: str) -> List[Citizen]:
        """Return a list of all citizens with the job <job>, in order of
        increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = DistrictLeader(3, "Starky Industries", 3024, "Labourer", 50,
        ... "Area Selen")
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.add_citizen(c6, 2)
        >>> o.add_citizen(c1, 4)
        >>> o.add_citizen(c3, 1)
        >>> o.add_citizen(c5, 1)
        >>> o.get_citizens_with_job('Manager') == [c1, c2, c4]
        True
        """

        lst = []
        citizens = self.get_all_citizens()  # get list of all citizens

        for citizen in citizens:  # check their job
            if citizen.job == job:
                lst = merge(lst, [citizen])  # merge with list
        return lst

    ###########################################################################
    # Task 2.3
    ###########################################################################
    def change_citizen_type(self, cid: int,
                            district_name: Optional[str] = None) -> Citizen:
        """Change the type of the Citizen with the given <cid>

        If the Citizen is currently a DistrictLeader, change them to become a
        regular Citizen (with no district name). If they are currently a regular
        Citizen, change them to become DistrictLeader for <district_name>.
        Note that this requires creating a new object of type either Citizen
        or DistrictLeader.

        The new Citizen/DistrictLeader should keep the same placement in the
        hierarchy (that is, the same superior and subordinates) that the
        original Citizen had, as well as the same ID, manufacturer, model year,
        job, and rating.

        Return the newly created Citizen/DistrictLeader.

        The original citizen that's being replaced should no longer be in the
        hierarchy (it should not be anyone's subordinate nor superior).

        Precondition:
        - If <cid> is the id of a DistrictLeader, <district_name> must be None
        - A citizen with the given <cid> exists in this hierarchy.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = DistrictLeader(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60,
        ... "Selen")
        >>> c4 = Citizen(4, "S.T.A.R. Lab", 3040, "Commander", 10)
        >>> c10 = Citizen(10, "S.T.A.R. Lab", 3041, "Commander", 20)
        >>> c11 = Citizen(11, "S.T.A.R. Lab", 3042, "Commander", 30)
        >>> o = Society()
        >>> o.add_citizen(c3)
        >>> o.add_citizen(c2, 3)
        >>> o.add_citizen(c1, 2)
        >>> o.add_citizen(c4, 3)
        >>> o.add_citizen(c10, 4)
        >>> o.add_citizen(c11, 4)
        >>> isinstance(c3, DistrictLeader)
        True
        >>> k = o.change_citizen_type(3)
        >>> isinstance(o.get_citizen(3), DistrictLeader)
        False
        >>> isinstance(o.get_citizen(3), Citizen)
        True
        >>> isinstance(c4, DistrictLeader)
        False
        >>> t = o.change_citizen_type(4, "Izmir")
        >>> isinstance(o.get_citizen(4), DistrictLeader)
        True
        >>> c10.get_district_name()
        'Izmir'
        """

        cit = self.get_citizen(cid)
        if isinstance(cit, DistrictLeader):
            subs = cit.get_direct_subordinates()
            sup = cit.get_superior()
            new_cit = Citizen(cit.cid, cit.manufacturer, cit.model_year,
                              cit.job, cit.rating)
            for s in subs:
                new_cit.add_subordinate(s)
            if sup is not None:
                sup.remove_subordinate(cit.cid)
                sup.add_subordinate(new_cit)
            else:
                self.set_head(new_cit)
            return new_cit
        else:
            subs = cit.get_direct_subordinates()
            sup = cit.get_superior()
            new_lead = DistrictLeader(cit.cid, cit.manufacturer,
                                      cit.model_year, cit.job,
                                      cit.rating, district_name)
            for s in subs:
                new_lead.add_subordinate(s)
            if sup is not None:
                sup.remove_subordinate(cit.cid)
                sup.add_subordinate(new_lead)
            else:
                self.set_head(new_lead)
        return new_lead

    ###########################################################################
    # Task 3.1
    ###########################################################################

    def _swap_up(self, citizen: Citizen) -> Citizen:
        """Swap <citizen> with their superior in this Society (they should
         swap their job, and their position in the tree, but otherwise keep
         all the same attribute data they currently have).

        If the superior is a DistrictLeader, the citizens being swapped should
        also switch their citizen type (i.e. the DistrictLeader becomes a
        regular Citizen and vice versa).

        Return the Citizen after it has been swapped up ONCE in the Society.

        Precondition:
        - <citizen> has a superior (i.e., it is not the head of this Society),
          and is not a DistrictLeader.
        """
        # Note: depending on how you implement this method, PyCharm may warn you
        # that this method 'may be static' -- feel free to ignore this
        # c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)

        c2 = citizen.get_superior()

        # if the superior is a DL
        if isinstance(c2, DistrictLeader):
            dist = c2.get_district_name()
            temp_c6 = DistrictLeader(citizen.cid, citizen.manufacturer,
                                     citizen.model_year, c2.job, citizen.rating,
                                     dist)
            temp_c2 = Citizen(c2.cid, c2.manufacturer, c2.model_year,
                              citizen.job, c2.rating)

            # add the direct subs of old dude to the new dude
            for sub in citizen.get_direct_subordinates():
                citizen.remove_subordinate(sub.cid)
                sub.become_subordinate_to(temp_c2)

            temp_c2.become_subordinate_to(temp_c6)

            # this could be problematic
            c2.remove_subordinate(citizen.cid)

            for sub in c2.get_direct_subordinates():
                c2.remove_subordinate(sub.cid)
                sub.become_subordinate_to(temp_c6)

            if not c2 == self._head:
                highest = c2.get_superior()
                highest.remove_subordinate(c2.cid)
                temp_c6.become_subordinate_to(highest)
            else:
                self._head = temp_c6

            return temp_c6

        else:  # if citizen
            temp_c6 = Citizen(citizen.cid, citizen.manufacturer,
                              citizen.model_year, c2.job, citizen.rating)
            temp_c2 = Citizen(c2.cid, c2.manufacturer, c2.model_year,
                              citizen.job, c2.rating)

            # add the direct subs of old dude to the new dude
            for sub in citizen.get_direct_subordinates():
                citizen.remove_subordinate(sub.cid)
                sub.become_subordinate_to(temp_c2)

            temp_c2.become_subordinate_to(temp_c6)

            # this could be problematic
            c2.remove_subordinate(citizen.cid)

            for sub in c2.get_direct_subordinates():
                c2.remove_subordinate(sub.cid)
                sub.become_subordinate_to(temp_c6)

            highest = c2.get_superior()
            highest.remove_subordinate(c2.cid)
            temp_c6.become_subordinate_to(highest)

            return temp_c6

    def promote_citizen(self, cid: int) -> None:
        """Promote the Citizen with cid <cid> until they either:
             - have a superior with a higher rating than them or,
             - become DistrictLeader for their district.
        See the Assignment 2 handout for further details.

        Precondition: There is a Citizen with the cid <cid> in this Society.
        """

        citizen = self.get_citizen(cid)
        if isinstance(citizen, DistrictLeader):
            return None

        elif self.get_head() == citizen:
            return None

        elif citizen.get_superior().rating >= citizen.rating:
            return None

        else:
            new = self._swap_up(citizen)
            self.promote_citizen(new.cid)
        return None

    ###########################################################################
    # Task 3.2
    ###########################################################################

    def delete_citizen(self, cid: int) -> None:
        """Remove the Citizen with ID <cid> from this Society.

        If this Citizen has subordinates, their subordinates become subordinates
        of this Citizen's superior.

        If this Citizen is the head of the Society, their most highly rated
        direct subordinate becomes the new head. If they did not have any
        subordinates, the society becomes empty (the society head becomes None).

        Precondition: There is a Citizen with the cid <cid> in this Society.
        """

        lst = self.get_all_citizens()

        # find target
        target = ''
        for citizen in lst:
            if citizen.cid == cid:
                target = citizen

        subs = Citizen.get_direct_subordinates(target)

        # if target to remove is head
        if target == self._head:
            if not subs:
                self._head = None
            else:
                new_head = Citizen.get_highest_rated_subordinate(target)
                target_subs = Citizen.get_direct_subordinates(target)

                _delete_citizen_helper(target_subs, new_head)

                self._head = new_head
                for sub in target_subs:
                    Citizen.add_subordinate(new_head, sub)

        # target is the guy to remove
        else:
            sup_target = Citizen.get_superior(target)
            subs = Citizen.get_direct_subordinates(target)
            Citizen.remove_subordinate(sup_target, target.cid)

            for sub in subs:
                Citizen.add_subordinate(sup_target, sub)
        return None


def _delete_citizen_helper(target_subs: List[Citizen],
                           new_head: Citizen) -> None:
    """Remove <new_head> from <target_subs>.
    """
    for cit in target_subs:
        if cit.cid == new_head.cid:
            target_subs.remove(cit)

###############################################################################
# Task 2: DistrictLeader
###############################################################################


class DistrictLeader(Citizen):
    """The leader of a district in a society.

    === Private Attributes ===
    _district_name:
        The name of the district that this DistrictLeader is the leader of.

    === Inherited Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Inherited Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - All Citizen RIs are inherited.
    """
    _district_name: str

    ###########################################################################
    # Task 2.1
    ###########################################################################
    def __init__(self, cid: int, manufacturer: str, model_year: int,
                 job: str, rating: int, district: str) -> None:
        """Initialize this DistrictLeader with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, rating <rating>, and
        district name <district>.

        >>> c2 = DistrictLeader(2, "Some Lab", 3024, "Lawyer", 30, "District A")
        >>> c2.manufacturer
        'Some Lab'
        >>> c2.get_district_name()
        'District A'
        """
        Citizen.__init__(self, cid, manufacturer, model_year, job, rating)
        self._district_name = district

    def get_district_citizens(self) -> List[Citizen]:
        """Return a list of all citizens in this DistrictLeader's district, in
        increasing order of cid.

        Include the cid of this DistrictLeader in the list.

        >>> c1 = DistrictLeader(
        ...     1, "Hookins National Lab", 3024, "Commander", 65, "District A"
        ... )
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Lawyer", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Labourer", 55)
        >>> c2.become_subordinate_to(c1)
        >>> c3.become_subordinate_to(c1)
        >>> c1.get_district_citizens() == [c1, c2, c3]
        True
        """
        lst = merge(self.get_all_subordinates(), [self])
        return lst

    ###########################################################################
    # Task 2.2
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the name of the district that this DistrictLeader leads.
        """
        return self._district_name

    def rename_district(self, district_name: str) -> None:
        """Rename this district leader's district to the given <district_name>.
        """
        self._district_name = district_name


###########################################################################
# ALL PROVIDED FUNCTIONS BELOW ARE COMPLETE, DO NOT CHANGE
###########################################################################
def create_society_from_file(file: TextIO) -> Society:
    """Return the Society represented by the information in file.

    >>> o = create_society_from_file(open('citizens.csv'))
    >>> o.get_head().manufacturer
    'Hookins National Lab'
    >>> len(o.get_head().get_all_subordinates())
    11
    """
    head = None
    people = {}
    for line in file:
        info: List[Any] = line.strip().split(',')
        info[0] = int(info[0])
        info[2] = int(info[2])
        info[4] = int(info[4])

        if len(info) == 7:
            inf = info[:5] + info[-1:]
            person = DistrictLeader(*inf)
        else:
            person = Citizen(*info[:5])

        superior = info[5]
        if not info[5]:
            head = person
            superior = None
        else:
            superior = int(superior)
        people[info[0]] = (person, superior)

    for key in people:
        if people[key][1] is not None:
            people[people[key][1]][0].add_subordinate(people[key][0])

    return Society(head)


###########################################################################
# Sample societies from the handout
###########################################################################
def simple_society_demo() -> Society:
    """Handout example related to a simple society.
    """
    c = Citizen(6, "Starky Industries", 3036, "Commander", 50)
    c2 = Citizen(2, "Hookins National", 3027, "Manager", 55)
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = Citizen(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17)
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def district_society_demo() -> Society:
    """Handout example related to a simple society with districts.
    """
    c = DistrictLeader(6, "Starky Industries", 3036, "Commander", 50, "Area 52")
    c2 = DistrictLeader(2, "Hookins National", 3027, "Manager", 55,
                        "Repair Support")
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17, "Finance")
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def promote_citizen_demo() -> Society:
    """Handout example related to promote_citizen.
    """
    c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
    c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 50, "Finance")
    c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
    c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
    c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 5)
    s.add_citizen(c4, 7)
    s.add_citizen(c5, 7)

    s.promote_citizen(11)
    return s


def create_from_file_demo() -> Society:
    """Handout example related to reading from the provided file citizens.csv.
    """
    return create_society_from_file(open("citizens.csv"))


if __name__ == "__main__":
    # As you complete your tasks, you can uncomment any of the function calls
    # and the print statement below to create and print out a sample society:
    soc = simple_society_demo()
    # soc = district_society_demo()
    # soc = promote_citizen_demo()
    # soc = create_from_file_demo()
    # print(soc)

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['typing', '__future__',
                                   'python_ta', 'doctest'],
        'disable': ['E9998', 'R0201'],
        'max-args': 7,
        'max-module-lines': 1600
    })
