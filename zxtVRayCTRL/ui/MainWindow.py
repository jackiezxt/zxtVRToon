# -*- coding: utf-8 -*-
"""
@author  : reliable-天
@contact : U{johnny.zxt@gmail.com<johnny.zxt@gmail.com>}
@website : http://zxto.top:1580
@gitlab  : http://zxto.top:30000
@software: PyCharm
@file    : zxtVRToon.py
@time    : 2020/1/3 0:41
"""

import sys
from functools import partial
import maya.api.OpenMaya as OpenMaya
import json

# import utils.zxtVRayCTRL_utils
from ..utils import zxtVRayCTRL_utils, renderSetup_utils

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

    is_maya_2018 = False
except:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    import maya.cmds as mc

    is_maya_2018 = True

    reload( zxtVRayCTRL_utils )
    import maya.app.renderSetup.model.override as override
    import maya.app.renderSetup.model.selector as selector
    import maya.app.renderSetup.model.collection as collection
    import maya.app.renderSetup.model.renderLayer as renderLayer
    import maya.app.renderSetup.model.renderSetup as renderSetup
    import maya.cmds as mc
    import maya.api.OpenMaya as om

    rs = renderSetup.instance()

    layers = rs.getRenderLayers()

    from ..ui.ToolBar_ui import zxtVRayToonToolBar


class MainWindow( QWidget ):
    def __init__(self):
        self._vr = zxtVRayCTRL_utils.zxtVRayCTRL()
        self._rl = renderSetup_utils
        self._filepath = 'T:/maya/Assets/M_AST/M_AST_vrRimGrad.ma'
        self.sel_list = None

        self.shd_list = None

        self.toon_mtl_list = None

        # 窗口固有属性-------------------------------
        super( MainWindow, self ).__init__()
        self.setWindowTitle( 'ZXTO_VrayToon工具' )  # 设置窗口标题
        self.resize( 1, 1 )  # 设置窗口尺寸
        self.setWindowFlags(
            self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint ) if is_maya_2018 else self.setWindowFlag(
            Qt.FramelessWindowHint, True )

        # 窗口实例化内容-------------------------------
        self.toolbar = zxtVRayToonToolBar()
        self.toolbar_ui = self.toolbar.get_ui()
        font = QFont()
        font.setPointSize(13)
        self.lb_title = QLabel( 'ZXTO 三渲二制作工具\n基础版' )
        self.lb_title.setFont(font)
        self.lb_title.setAlignment((Qt.AlignCenter))

        self.lb_title.setGeometry(10,10,300,20)
        self.lb_email = QLabel('有问题联系：johnny.zxt@gmail.com')

        # self.btn_ref = QPushButton( '第0步: 创建ASSET' )
        # self.btn_connect_toon_switch = QPushButton( '第一步：连接switch材质' )
        # self.btn_add_vray_attr = QPushButton( '第二步：创建vray属性' )
        # self.btn_add_custom_aov = QPushButton( '第三步：添加自制的AOV' )
        # self.btn_add_box = QPushButton( '第四步：添加渐变盒子' )
        # self.btn_close = QPushButton( '关闭' )
        # 窗口布局layout-------------------------------
        main_layout = QVBoxLayout()
        main_layout.setSpacing( 0 )

        self.setLayout( main_layout )

        main_layout.addWidget( self.lb_title )
        main_layout.addWidget( self.toolbar_ui )
        main_layout.addWidget(self.lb_email)

        # 连接信号
        self.toolbar_ui.btn_select.clicked.connect( self.set_sel_list )
        self.toolbar_ui.btn_ref.clicked.connect( partial( self._referenceFile, self._filepath ) )
        self.toolbar_ui.btn_render_layer.clicked.connect( partial( self.setRenderLayer ) )

        self.toolbar_ui.btn_connect_toon_switch.clicked.connect(self.connectSHDtoSWT)
        # self.toolbar_ui.btn_add_vray_attr.clicked.connect(
        #     partial( self._vr.addVRayAttr, partial(self.getToonMtlList, 'VRayToonMtl') ) )
        self.toolbar_ui.btn_add_custom_aov.clicked.connect( self.addCustomAOV )
        self.toolbar_ui.btn_add_box.clicked.connect( partial( self._vr.addBox, 3 ) )
        self.toolbar_ui.btn_close.clicked.connect( self.close )

        self._last_mouse_pos = None
        self._current_mouse_pos = None
        self._is_moving = False

    def set_sel_list(self):
        self.sel_list = mc.ls( sl = True, type = 'transform' )
        return self.sel_list

    def get_sel_list(self):
        return self.sel_list

    def set_shd_list(self, sellist):
        self.shd_list = self._vr.ShadList( sellist )
        return self.shd_list

    def get_shd_list(self):
        return self.shd_list

    def MtlList(self, shaderType):
        sl = self.get_sel_list()
        # print( "getToonMtlList====%s"%sl )
        # self.set_shd_list( sl )
        shdlist = self.set_shd_list( sl )
        clean_shdList = list( set( shdlist ) )
        self.toon_mtl_list = self._vr.GetWantedType( clean_shdList, shaderType )
        return self.toon_mtl_list

    def getToonMtlList(self):
        print('getToonMtlList=====%s'%(self.MtlList('VRayToonMtl')))
        return self.MtlList('VRayToonMtl')

    def getVRayMtl(self):
        ddd = self.MtlList('VRayMtl')
        print('getVRayMtl=====%s'%ddd)
        return ddd

    def connectSHDtoSWT(self):
        rd = rs.getDefaultRenderLayer()
        r_real_lig = rs.getRenderLayer('real_lig')
        rs.switchToLayer( r_real_lig )
        c_real_lig_1 = r_real_lig.getCollectionByName('cha_rl')
        c_real_lig_2 = c_real_lig_1.getCollectionByName('cha_rl_shadingEngines')
        o_real_lig = c_real_lig_2.getOverrides()
        o_real_lig[1].setSelfEnabled(0)
        c_real_lig_2.setIsolateSelected(1)

        self._vr.connectToonSwt(self.getVRayMtl())

        o_real_lig[1].setSelfEnabled( 1 )
        c_real_lig_2.setIsolateSelected( 0 )
        rs.switchToLayer(rd)

    def setRenderLayer(self):

        rl_cha_common = rs.createRenderLayer( "cha_common" )
        c_cha_common = rl_cha_common.createCollection( "cha_cc" )
        c_cha_common.getSelector().setPattern( 'Geometry,::Geometry' )

        rl_real_lig = rs.createRenderLayer( 'real_lig' )
        c_real_lig = rl_real_lig.createCollection( "cha_rl" )
        c_real_lig.getSelector().setPattern( 'Geometry,::Geometry' )


        # c_real_lig_shd_over = c_real_lig.createCollection( "cha_rl_shd_over" )
        # c_real_lig_shd_over.getSelector().setPattern( '*' )  # 这是以表达式来添加
        # c_real_lig_shd_over.getSelector().setFilterType( selector.Filters.kShaders )
        # c_real_lig_shd_over.getSelector().staticSelection.set(['pCube1','pCube2']) # 这是以物件名称添加

        zxtVrayRL_shader = mc.shadingNode( 'VRayMtl', name = 'zxtVrayRL', asShader = True )  # 创建一个vrayMtl用来override
        mc.setAttr( 'zxtVrayRL.color', 0, 0, 0, type = 'double3' )

        # c_real_lig_shd_over.createOverride( "zxtVRayMtl_over", "materialOverride" )  ## 这里先要建立vrayMtl
        mtl_override = c_real_lig.createOverride( "zxtVRayMtl_over", OpenMaya.MTypeId( 0x58000386 ) )

        zxtoOut_override = c_real_lig.createOverride( "zxtoMtl_over", OpenMaya.MTypeId( 0x58000386 ) )

        mc.defaultNavigation( connectToExisting = True, source = 'zxtVrayRL',
                              destination = 'zxtVRayMtl_over.attrValue' )

        mc.defaultNavigation(connectToExisting = True, source = 'M_AST_vrRimGrad:M_AST_vrRimGrad_out', destination = 'zxtoMtl_over.attrValue')

        attr_names = ['diffuseColor', 'illumColor', 'reflectionColor']
        one_shader = self.MtlList('VRayToonMtl')
        if one_shader is not None:
            self._rl.renderlyr_SHDattr_override( 'toon_shadow', 'cha_ts', 'Geometry,::Geometry', '*', one_shader[0],
                                                 attr_names )
            mc.setAttr( '{}.attrValue'.format( attr_names[0] ), 1, 1, 1, type = 'double3' )

    def _referenceFile(self, filepath):
        ns = "M_AST_vrRimGrad"
        mc.file( filepath, reference = True, mergeNamespacesOnClash = False, namespace = ns, options = 'v=0;' )
        # file -r -type "mayaAscii"  -ignoreVersion -gl
        # -mergeNamespacesOnClash false -namespace "M_AST_vrRimGrad"
        # -options "v=0;" "T:/maya/Assets/M_AST/M_AST_vrRimGrad.ma";

    def addCustomAOV(self):
        self._vr.addCustomAOV()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            g_pos = QCursor.pos()
            self._last_mouse_pos = g_pos
            self._current_mouse_pos = g_pos
            self._is_moving = True

    def mouseMoveEvent(self, event):
        if self._is_moving:
            g_pos = QCursor.pos()
            self._current_mouse_pos = g_pos
            self.move( self.pos() + self._current_mouse_pos - self._last_mouse_pos )
            self._last_mouse_pos = self._current_mouse_pos

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self._last_mouse_pos = None
            self._current_mouse_pos = None
            self._is_moving = False

        # ----------------以上是鼠标右键移动窗口代码
