
from sc2simulator.scenarioMgr.scenarioPlayer import ScenarioPlayer
from sc2simulator.scenarioMgr.scenarioUnit import ScenarioUnit


################################################################################
class Scenario(object):
    ############################################################################
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.units = {}
        self.upgrades = {}
        self.startloop = 1
        self.duration = 0.0
    ############################################################################
    def __str__(self):  return self.__repr__()
    def __repr__(self):
        return "<%s '%s' players:%s>"%(self.__class__.__name__,
            self.name, list(self.players.keys()))
    ############################################################################
    def addPlayer(self,idx):
        idx = int(idx) # ensure value is an integer
        if idx in self.players:
            print("WARNING: attempted to add already existing player %d: %s"%(
                idx, self.players[idx]))
            return self.players[idx]
        upgradeList = []
        self.upgrades[idx] = upgradeList
        p = ScenarioPlayer(idx, self.units, upgradeList)
        self.players[idx] = p
    ############################################################################
    def addUnit(self, tag):
        tag = int(tag) # ensure unit uid is always an integer
        if tag in self.units: # catch possible redundant definitions
            print("WARNING: unit tag %d already exists in %s as %s"%(
                tag, self, self.units[tag]))
            return
        newUnit = ScenarioUnit(tag)
        self.unts[tag] = newUnit
        return newUnit
    ############################################################################
    def addUpgrade(self, player, upgradeName):
        if player not in self.players:
            self.addPlayer(player)
        self.upgrades[player].append(upgradeName)
    ############################################################################
    def updateUnit(self, tag, **attrs):
        try:                u = self.units[tag] # lookup previously defined unit
        except KeyError:    u = self.addUnit(tag) # define a new unit
        for k,v in attrs.items(): # assign attributes into unit
            setattr(u, k, v)
        if u.player and u.player not in self.players: # ensure that this unit's owner is represented as a player
            self.addPlayer(u.player)
        return u
