# zxtVRToon


这是项目中临时使用的镜头制作工具包
其中分两个part
## Asset Part
这个部分主要是在镜头制作中用来reference的文件，目录地址放置在：`T:\maya`目标下
## zxtVRayCTRL Part
这个部分主要是工具，用于在maya中执行，下载下来后，放在一个随便什么空文件下，比如放在：`d:\plugins`下，然后将maya.env和userSetup,以及zxtVRayCTRL.mod文件，根据自己的工作环境放在相对应的目录下面，
1. maya.env中的路径 
```
MAYA_MODULE_PATH = C:\Users\johnnyzxt\Documents\maya\2018\modules   ///这个路径根据自己的修改，这个文件夹下，放zxtVRayCTRL.mod文件
PYTHONPATH=%PYTHONPATH%;d:\plugins   ///这里的地址根据自己的电脑修改

```
2.userSetup.py中的路径
在第11行，将p_path 修改为自己的下载这个脚本位置，比如`d:\plugins`

3.zxtVRayCTRL.mod文件中的路径
`+ zxtVRayCTRL			d:\plugins\zxtVRayCTRL`  将这一句后面的路径修改为自己放置脚本的路径，比如`d:\plugins\zxtVRayCTRL`

4.接在在maya窗口中执行
![](http://www.zxto.top:30000//johnny/mypicgo/uploads/6ca6484b3b9e02da2c882b9f9d427297/20200312032835.png)
```python
import sys

import zxtVRayCTRL.zxtVRayToon
reload(zxtVRayCTRL.zxtVRayToon)

zxtVRayCTRL.zxtVRayToon.run()

```

**maya版本**：2018.5

**V-ray**: V-Ray Next v4.12.02

**操作系统**：win10 1903版本以上

**MSCV版本**：14.2

**PYTHON版本**：2.7

**Cython版本**：0.29