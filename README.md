# Blender-uvar
auto reload UV by filechange event

tested with python 3.6.2 on windows 10

# Dependencies
* watchdog 0.8.3
* pathtools 0.1.2

# Installation steps
* pip3 install watchdog
* pip3 install pathtools
* python -m site
* find and open %YOUR_PYTHON_PATH%\lib\site-packages
* copy watchdog, pathtools directory into %YOUR_BLENDER_FOLDER%\%YOUR_BLENDER_VERSION%\python\lib\site-packages
* install addon in blender preferences
* use it from UV/Image Editor > Tool Shelf > UV Autoreload


![tutorial gif](https://github.com/noa-ru/blender-uvar/blob/master/tutorial.gif?raw=true)
