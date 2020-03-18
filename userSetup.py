print("the userSetup.py is running")
import maya.cmds as mc
import maya.cmds as cmds
import maya.utils as utils
import os

import sys
import pymel.core as pm
import maya.mel as mel

p_path = ['d:/plugins']
for pa in p_path:
	sys.path.append(pa)

