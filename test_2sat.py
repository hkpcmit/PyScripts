#!/opt/local/bin/pypy


import test_scc
import unittest2


class Error(Exception):
    """Base error class."""


class TwoSat(object):

    def __init__(self):
        self.scc = test_scc.SccGraphStack()
        self.var_set = set()
        self.clause_list = []

    def AddClause(self, var1, var2):
        self.clause_list.append([var1, var2])
        self.var_set.add(var1)
        self.var_set.add(var2)

    def CheckVarNegation(self, scc):
        # Store negations desired by previous iteration of vars.
        negation_set = set()
        for var in scc:
            if var in negation_set:
                # SCC contains negation of a var.
                return True
            negation_set.add(-var)
        return False

    def InsertClauses(self):
        for var1, var2 in self.ReduceClauses():
            self.scc.AddEdge(-var1, var2)
            self.scc.AddEdge(-var2, var1)

    def IsSatisfiable(self):
        self.InsertClauses()
        for scc in self.scc.GetSccList():
            if len(scc) <= 1:
                continue
            if self.CheckVarNegation(scc):
                # Cannot satisfy assignment of both var and its negation.
                return False
        return True

    def ReduceClauses(self):
        old_clauses, new_clauses = [], self.clause_list
        old_var_set, new_var_set = None, self.var_set
        while len(old_clauses) != len(new_clauses):
            old_clauses, new_clauses = new_clauses, []
            old_var_set, new_var_set = new_var_set, set()
            # Try to skip clauses that contain either var and -var but not both.
            # These clauses can be satisfied by setting var to 0/1 appropriately.
            for var1, var2 in old_clauses:
                if (-var1 in old_var_set) and (-var2 in old_var_set):
                    new_clauses.append([var1, var2])
                    new_var_set.add(var1)
                    new_var_set.add(var2)
        return new_clauses


class TwoSatTest(unittest2.TestCase):
        
    def testSingleVarTrue(self):
        two_sat = TwoSat()
        two_sat.AddClause(1, 1)
        self.assertTrue(two_sat.IsSatisfiable())

    def test2SatFalse1(self):
        two_sat = TwoSat()
        clauses = [(-1, 2), (-2, -1), (1, -2), (2, 1)]
        for clause in clauses:
            two_sat.AddClause(*clause)
        self.assertFalse(two_sat.IsSatisfiable())

    def test2SatFalse2(self):
        two_sat = TwoSat()
        clauses = [(2, 4), (1, 2), (-1, 2), (-2, 1), (-1, -2)]
        for clause in clauses:
            two_sat.AddClause(*clause)
        self.assertFalse(two_sat.IsSatisfiable())

    def test2SatTrue1(self):
        two_sat = TwoSat()
        clauses = [(1, 2), (-2, 3), (-1, -2), (3, 4),
                   (-3, 5), (-4, -5), (-3, 4)]
        for clause in clauses:
            two_sat.AddClause(*clause)
        self.assertTrue(two_sat.IsSatisfiable())

    def test2SatTrue2(self):
        two_sat = TwoSat()
        clauses = [(4, 5), (1, 2), (2, 3), (3, 4),
                   (-1, -3), (-2, -4)]
        for clause in clauses:
            two_sat.AddClause(*clause)
        self.assertTrue(two_sat.IsSatisfiable())

    def test2SatTrue3(self):
        two_sat = TwoSat()
        clauses = [(8, 12), (1, 4), (-2, 5), (3, 7), (2, -5),
                   (-8, -2), (3, -1), (4, -3), (-3, -7), (6, 7),
                   (1, 7), (-7, -1)]
        for clause in clauses:
            two_sat.AddClause(*clause)
        self.assertTrue(two_sat.IsSatisfiable())


class TwoSatHWTest(unittest2.TestCase):

    def GetInstance(self, file_name):
        two_sat = TwoSat()
        with open(file_name, 'r') as fd:
            for _ in xrange(int(fd.readline())):
                line = fd.readline()
                two_sat.AddClause(*(int(l) for l in line.split()))
        return two_sat
                
    def testHW1(self):
        two_sat = self.GetInstance('2sat1.txt')
        self.assertTrue(two_sat.IsSatisfiable())
                
    def testHW2(self):
        two_sat = self.GetInstance('2sat2.txt')
        self.assertFalse(two_sat.IsSatisfiable())
                
    def testHW3(self):
        two_sat = self.GetInstance('2sat3.txt')
        self.assertTrue(two_sat.IsSatisfiable())
                
    def testHW4(self):
        two_sat = self.GetInstance('2sat4.txt')
        self.assertTrue(two_sat.IsSatisfiable())
                
    def testHW5(self):
        two_sat = self.GetInstance('2sat5.txt')
        self.assertFalse(two_sat.IsSatisfiable())
                
    def testHW6(self):
        two_sat = self.GetInstance('2sat6.txt')
        self.assertFalse(two_sat.IsSatisfiable())


if __name__ == '__main__':
    unittest2.main()

