from typing import Any
import random
import time


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.

        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """

        self.variables = variables
        self.domains = domains
        self.edges = edges
        self.assignments: dict[str, Any] = {}

        self.numberOfFailures = 0
        self.numberOfBacktracks = 0

        # add already assigned variables to the assignments
        for key, value in self.domains.items():
            if len(value) == 1:
                self.assignments[key] = list(value)[0]

        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add(
                            (value1, value2)
                        )
                        self.binary_constraints[(variable1, variable2)].add(
                            (value2, value1)
                        )

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.

        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """

        for edge in self.edges:
            domain1 = self.domains[edge[0]]  # Domain of variable 1
            domain2 = self.domains[edge[1]]  # Domain of variable 2

            newDomain1 = set()
            newDomain2 = set()

            # Iterate over all possible combinations of values from domain1 and domain2
            for value1 in domain1:
                for value2 in domain2:
                    # Check if the values are different
                    if value1 != value2:
                        # Add the values to the new domains
                        newDomain1.add(value1)
                        newDomain2.add(value2)

            # Update the domains with the new values
            self.domains[edge[0]] = newDomain1
            self.domains[edge[1]] = newDomain2

    def backtracking_search(self, visualizer=None) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """

        def backtrack():
            self.numberOfBacktracks += 1
            # Check if the current assignment is consistent
            if not self.isConsistent():
                self.numberOfFailures += 1
                return None

            # Select an unassigned variable
            newVariable = self.select_unassigned()
            if newVariable is None:
                return self.assignments

            possibleDomains = list(self.domains[newVariable])

            # UNCOMMENT this to shuffle the domains for possibility of faster runtime
            random.shuffle(possibleDomains)

            for domain in possibleDomains:
                # Try assigning values from the domain of the selected variable
                self.assignments[newVariable] = domain

                if visualizer is not None:  # Visualizer specific for the sudoku problem
                    visualizer.update_board(
                        self.assignments, self.numberOfBacktracks, self.numberOfFailures
                    )

                # Recursively call backtrack
                res = backtrack()

                if res is None:
                    # If the assignment is not consistent, backtrack
                    del self.assignments[newVariable]
                    continue

                if self.isAllAssigned():
                    # If all variables are assigned, return the assignments
                    return self.assignments

            # If no solution was found, backtrack
            self.numberOfFailures += 1
            return None

        return backtrack()

    def unassigned(self) -> list[str]:
        """Returns a list of unassigned variables

        Returns
        -------
        list[str]
            List of unassigned variables
        """
        unassigned = []

        for variable in self.variables:
            if not self.assignments.get(variable, None):
                unassigned.append(variable)

        return unassigned

    def isConsistent(self) -> bool:
        """
        Returns True if the current assignment is consistent, otherwise False.
        """
        for edge in self.edges:
            assignedValues = [
                self.assignments.get(edgeVariable, None) for edgeVariable in edge
            ]  # fetch the assigned variable from each edge, return None if not assigned

            # Checks if any of the edges has been assigned a value and if those values are equal
            if len(assignedValues) != len(set(assignedValues)) and all(assignedValues):
                return False

        return True

    def isAllAssigned(self):
        """Returns True if all variables are assigned, otherwise False"""

        for variable in self.variables:
            if not self.assignments.get(variable, None):
                return False

        return True

    def select_unassigned(self):
        """
        Returns an unassigned variable, or None if all variables are assigned.
        """
        unassignedValues = self.unassigned()
        if len(unassignedValues) == 0:
            return None
        # Choosing a random unassigned variable results very long runtimes on some problems
        # return random.choice(unassignedValues)

        # Choosing the first unassigned variable results in a faster runtime on most problems
        return unassignedValues[0]


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables

    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [
        (variables[i], variables[j])
        for i in range(len(variables) - 1)
        for j in range(i + 1, len(variables))
    ]


def test():
    variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]

    csp = CSP(
        variables=variables,
        domains={variable: {"red", "green", "blue"} for variable in variables},
        edges=[
            ("SA", "WA"),
            ("SA", "NT"),
            ("SA", "Q"),
            ("SA", "NSW"),
            ("SA", "V"),
            ("WA", "NT"),
            ("NT", "Q"),
            ("Q", "NSW"),
            ("NSW", "V"),
        ],
    )

    csp.ac_3()
    print(csp.backtracking_search())
    print(csp.isConsistent())


if __name__ == "__main__":
    test()
