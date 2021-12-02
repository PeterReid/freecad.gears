# -*- coding: utf-8 -*-
# ***************************************************************************
# *                                                                         *
# * This program is free software: you can redistribute it and/or modify    *
# * it under the terms of the GNU General Public License as published by    *
# * the Free Software Foundation, either version 3 of the License, or       *
# * (at your option) any later version.                                     *
# *                                                                         *
# * This program is distributed in the hope that it will be useful,         *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of          *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           *
# * GNU General Public License for more details.                            *
# *                                                                         *
# * You should have received a copy of the GNU General Public License       *
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.   *
# *                                                                         *
# ***************************************************************************

import os
import FreeCAD
import FreeCADGui as Gui
from .features import ViewProviderGear, InvoluteGear, InternalInvoluteGear, InvoluteGearRack, CycloidGearRack
from .features import CycloidGear, BevelGear, CrownGear, WormGear, TimingGear, LanternGear, HypoCycloidGear, BaseGear
from .connector import GearConnector, ViewProviderGearConnector


class BaseCommand(object):
    NAME = ""
    GEAR_FUNCTION = None
    ICONDIR = os.path.join(os.path.dirname(__file__), "icons")

    def __init__(self):
        pass

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        Gui.doCommandGui("import freecad.gears.commands")
        Gui.doCommandGui("freecad.gears.commands.{}.create()".format(
            self.__class__.__name__))
        FreeCAD.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")

    @classmethod
    def create(cls):
        if FreeCAD.GuiUp:
            # borrowed from threaded profiles
            # puts the gear into an active container
            body = Gui.ActiveDocument.ActiveView.getActiveObject("pdbody")
            part = Gui.ActiveDocument.ActiveView.getActiveObject("part")

            if body:
                obj = FreeCAD.ActiveDocument.addObject("PartDesign::FeaturePython", cls.NAME)
            else:
                obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.NAME)
            ViewProviderGear(obj.ViewObject, cls.Pixmap)
            cls.GEAR_FUNCTION(obj)

            if body:
                body.addObject(obj)
            elif part:
                part.Group += [obj]
        else:
            obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", cls.NAME)
            cls.GEAR_FUNCTION(obj)
        return obj

    def GetResources(self):
        return {'Pixmap': self.Pixmap,
                'MenuText': self.MenuText,
                'ToolTip': self.ToolTip}


class CreateInvoluteGear(BaseCommand):
    NAME = "involutegear"
    GEAR_FUNCTION = InvoluteGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'involutegear.svg')
    MenuText = 'Involute gear'
    ToolTip = 'Create an external involute gear'


class CreateInternalInvoluteGear(BaseCommand):
    NAME = "internalinvolutegear"
    GEAR_FUNCTION = InternalInvoluteGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'internalinvolutegear.svg')
    MenuText = 'Internal involute gear'
    ToolTip = 'Create an internal involute gear'


class CreateInvoluteRack(BaseCommand):
    NAME = "involuterack"
    GEAR_FUNCTION = InvoluteGearRack
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'involuterack.svg')
    MenuText = 'Involute rack'
    ToolTip = 'Create an Involute rack'

class CreateCycloidRack(BaseCommand):
    NAME = "Cycloidrack"
    GEAR_FUNCTION = CycloidGearRack
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'cycloidrack.svg')
    MenuText = 'Cycloid rack'
    ToolTip = 'Create an Cycloid rack'


class CreateCrownGear(BaseCommand):
    NAME = "crowngear"
    GEAR_FUNCTION = CrownGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'crowngear.svg')
    MenuText = 'Crown gear'
    ToolTip = 'Create a Crown gear'


class CreateCycloidGear(BaseCommand):
    NAME = "cycloidgear"
    GEAR_FUNCTION = CycloidGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'cycloidgear.svg')
    MenuText = 'Cycloid gear'
    ToolTip = 'Create a Cycloid gear'


class CreateBevelGear(BaseCommand):
    NAME = "bevelgear"
    GEAR_FUNCTION = BevelGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'bevelgear.svg')
    MenuText = 'Bevel gear'
    ToolTip = 'Create a Bevel gear'

class CreateHypoCycloidGear(BaseCommand):
    NAME = "hypocycloidgear"
    GEAR_FUNCTION = HypoCycloidGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'hypocycloidgear.svg')
    MenuText = 'HypoCycloid gear'
    ToolTip = 'Create a HypoCycloid gear with its pins'


class CreateWormGear(BaseCommand):
    NAME = "wormgear"
    GEAR_FUNCTION = WormGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'wormgear.svg')
    MenuText = 'Worm gear'
    ToolTip = 'Create a Worm gear'


class CreateTimingGear(BaseCommand):
    NAME = "timinggear"
    GEAR_FUNCTION = TimingGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'timinggear.svg')
    MenuText = 'Timing gear'
    ToolTip = 'Create a Timing gear'

class CreateLanternGear(BaseCommand):
    NAME = "lanterngear"
    GEAR_FUNCTION = LanternGear
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'lanterngear.svg')
    MenuText = 'Lantern gear'
    ToolTip = 'Create a Lantern gear'

class CreateGearConnector(BaseCommand):
    NAME = "gearconnector"
    GEAR_FUNCTION = GearConnector
    Pixmap = os.path.join(BaseCommand.ICONDIR, 'gearconnector.svg')
    MenuText = 'Combine two gears'
    ToolTip = 'Combine two gears'

    def Activated(self):
        gear1 = Gui.Selection.getSelection()[0]
        assert isinstance(gear1.Proxy, BaseGear)

        gear2 = Gui.Selection.getSelection()[1]
        assert isinstance(gear2.Proxy, BaseGear)

        # check if selected objects are beams

        obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", self.NAME)
        GearConnector(obj, gear1, gear2)
        ViewProviderGearConnector(obj.ViewObject)

        FreeCAD.ActiveDocument.recompute()
        return obj
