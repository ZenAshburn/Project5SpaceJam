from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage

class Dumbledore(SphereCollideObject):

    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):

        super(Dumbledore, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.32, -0.25, 0), 1.0)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex,1)

        self.reloadTime = 0.25
        self.missileDistance = 4000
        self.missileBay = 1

        base.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        self.SetKeyBindings()
        self.EnableHUD()
        
    def Thrust(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyThrust, 'forward-thrust')
            
        else:
            base.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):

        rate = 5
        trajectory = base.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont

    def LeftTurn(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyLeftTurn, 'left-turn')

        else:
            base.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):

        rate = -0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def RightTurn(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyRightTurn, 'right-turn')

        else:
            base.taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):

        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def Climb(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyClimb, 'climb')

        else:
            base.taskMgr.remove('climb')

    def ApplyClimb(self, task):

        rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def Dive(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyDive, 'dive')

        else:
            base.taskMgr.remove('dive')
    
    def ApplyDive(self, task):

        rate = -0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def LeftRoll(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyLeftRoll, 'left-roll')

        else:
            base.taskMgr.remove('left-roll')

    def ApplyLeftRoll(self, task):

        rate = -0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RightRoll(self, keyDown):

        if keyDown:
            base.taskMgr.add(self.ApplyRightRoll, 'right-roll')

        else:
            base.taskMgr.remove('right-roll')

    def ApplyRightRoll(self, task):

        rate = 0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def Fire(self):
        if self.missileBay:
            
            travRate = self.missileDistance

            aim = base.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()

            fireSolution = aim * travRate
            inFront = aim * 150

            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + inFront

            currentMissile = Missile(base.loader, './Assets/Phaser/phaser.egg', base.render, tag, posVec, 4.0)
            
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)

            Missile.Intervals[tag].start()

        else:

            if not base.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')

                base.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
            
    def Reload(self, task):
        if task.time > self.reloadTime:

            self.missileBay += 1

            if self.missileBay > 1:
                self.missileBay = 1
            
            print("Reload complete.")

            return Task.done
        
        elif task.time <= self.reloadTime:
            print('Reload proceeding...')
            return Task.cont
        
    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()

                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]

                print(i + ' has reached the end of its fire solution.')

                break
        
        return Task.cont
    
    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
           
    def SetKeyBindings(self):
    
        base.accept("space", self.Thrust, [1])
        base.accept("space-up", self.Thrust, [0])
        base.accept("d", self.LeftTurn, [1])
        base.accept("d-up", self.LeftTurn, [0])
        base.accept("a", self.RightTurn, [1])
        base.accept("a-up", self.RightTurn, [0])
        base.accept("w", self.Climb, [1])
        base.accept("w-up", self.Climb, [0])
        base.accept("s", self.Dive, [1])
        base.accept("s-up", self.Dive, [0])
        base.accept("q", self.LeftRoll, [1])
        base.accept("q-up", self.LeftRoll, [0])
        base.accept("e", self.RightRoll, [1])
        base.accept("e-up", self.RightRoll, [0])
        base.accept("f", self.Fire)

