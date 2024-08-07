from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as spaceJamClasses
import Player as playerClasses
import DefensePaths as defensePaths
from math import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher

class MyApp(ShowBase):

    def __init__(self):
        
        ShowBase.__init__(self)
        self.SetupScene()

        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Station, nickName, j, fullCycle, 2)
            self.DrawxCircle(self.Planet6, nickName, j, fullCycle, 2)
            self.DrawyCircle(self.Planet6, nickName, j, fullCycle, 2)
            self.DrawzCircle(self.Planet6, nickName, j, fullCycle, 2)

        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Dumbledore.collisionNode, self.Dumbledore.modelNode)
        self.cTrav.addCollider(self.Dumbledore.collisionNode, self.pusher)

        self.cTrav.show_collisions(self.render)

    def SetupScene(self):
        
        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/starfield-in-blue.jpg", (0, 0, 0), 15000)
        # self.Universe.setHpr(173, 123, 37)

        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet1", "./Assets/Planets/tex1.jpg", (1720, 72, 1900), 150)
        # self.Planet1.setHpr(146, 19, 1)

        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet2", "./Assets/Planets/tex2.jpg", (2500, 4000, 2), 100)
        # self.Planet2.setHpr(132, 102, 142)

        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet3", "./Assets/Planets/tex3.jpg", (-1600, 3200, -30), 100)
        # self.Planet3.setHpr(4, 63, 124)

        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet4", "./Assets/Planets/tex4.jpg", (630, -4100, -3000), 200)
        # self.Planet4.setHpr(46, 31, 115)
        
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet5", "./Assets/Planets/tex5.jpg", (937, -8531, 5650), 250)
        # self.Planet5.setHpr(60, 36, 85)
        
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet6", "./Assets/Planets/tex6.jpg", (150, 5000, 67), 300)
        # self.Planet6.setHpr(136, 61, 4)
        
        self.Planet7 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, "Planet7", "./Assets/Planets/tex7.jpg", (1750, -1200, -1500), 350)
        # self.Planet7.setHpr(155, 27, 76)

        self.Dumbledore = playerClasses.Dumbledore(self.loader, self.taskMgr, self.accept, "./Assets/Spaceships/Dumbledore/Dumbledore.egg", self.render, "Dumbledore", "./Assets/Spaceships/Dumbledore/spacejet_C.png", (0, 0, 0), 2)

        self.Station = spaceJamClasses.SpaceStation(self.loader, "./Assets/SpaceStation/SpaceStation1B/spaceStation.egg", self.render, "Station", "./Assets/SpaceStation/SpaceStation1B/SpaceStation1_Dif2.png", (353, 375, 208), 5)
        # self.Station.setHpr(102, 29, 18)

        self.SetCamera()

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 80 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 2)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawxCircle(self, centralObject, droneName, step, numDrones, radius = 1):
        unitVec = defensePaths.xCircle(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawyCircle(self, centralObject, droneName, step, numDrones, radius = 1):
        unitVec = defensePaths.yCircle(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawzCircle(self, centralObject, droneName, step, numDrones, radius = 1):
        unitVec = defensePaths.zCircle(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
    
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Dumbledore.modelNode)
        self.camera.setFluidPos(0.32, -12, 0.75)

app = MyApp()
app.run()