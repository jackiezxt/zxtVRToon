import maya.cmds as mc


def buildSubdive():
    mm.eval('$meshName = `ls -sl`;\
    $shape = `listRelatives -f -s $meshName`;\
    for ($s = 0; $s < size($shape); ++$s)\
    {\
        vray   addAttributesFromGroup $shape[$s]   "vray_subdivision" 1;\
        vray   addAttributesFromGroup $shape[$s]   "vray_subquality"  1;\
        setAttr ($shape[$s] + ".vrayEdgeLength") 1.5;\
    }')


def deleSubdive():
    mm.eval('$meshName = `ls -sl`;\
    $shape = `listRelatives -f -s $meshName`;\
    for ($s = 0; $s < size($shape); ++$s)\
    {\
        vray   addAttributesFromGroup $shape[$s]   "vray_subdivision" 0;\
        vray   addAttributesFromGroup $shape[$s]   "vray_subquality"  0;\
    }')


def buildSubdiveWinUI():
    meshName = mc.ls(sl=1)
    shapes = mc.listRelatives(meshName, f=1, s=1)
    if mc.window('zxtBuildSub', ex=1):
        mc.deleteUI('zxtBuildSub', wnd=1)
    mc.window('zxtBuildSub', t='Vray批量添加细分', widthHeight=(
        250, 250), s=0, resizeToFitChildren=1, mnb=0, mxb=0)
    mc.columnLayout(adj=1)
    mc.text(label='先在视图窗口中框选要添加属性的polygon模型')
    mc.separator(height=5, style='in')
    mc.button(label='添加细分属性', c=buildSubdive)
    mc.button(label='删除细分属性', c=deleSubdive)
    subdieveSlider1 = mc.floatSliderGrp(label='Edge Length', field=True, fieldMinValue=0, fieldMaxValue=20, minValue=0,
                                        maxValue=20, value=0)
    subdieveSlider2 = mc.intSliderGrp(label='Max subdivs', field=True, fieldMinValue=4, fieldMaxValue=512, minValue=4,
                                      maxValue=512, value=4)
    mc.button(label='修改细分属性', c=lambda x: setSubValue(
        subdieveSlider1, subdieveSlider2))

    mc.showWindow()
