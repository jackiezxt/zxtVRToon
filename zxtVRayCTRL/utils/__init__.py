import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.cmds as mc
import maya.api.OpenMaya as om

rs = renderSetup.instance()

layers = rs.getRenderLayers()