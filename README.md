# zxtVRToon


这是项目中临时使用的镜头制作工具包
其中分两个part
## Asset Part
这个部分主要是在镜头制作中用来reference的文件，目录地址放置在：`T:\maya`目标下
## zxtVRayCTRL Part
这个部分主要是工具，用于在maya中执行，下载下来后，放在一个随便什么空文件下，比如放在：`c:\abcdefg`下，然后在maya窗口中执行

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