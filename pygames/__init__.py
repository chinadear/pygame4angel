#  pygame 打包方法
# 1.下载安装pyinstaller
# 2.找到安装目录一般在安装目录的Scripts文件夹下，找到pyinstaller.exe
# 3.将要打包的文件拷贝到pyinstaller.exe同目录下
# 4.cmd 进入pyinstaller.exe目录，执行pyinstaller -w -F blackandwhite.py(games.py是当前打包的内容，-w是单个文件，-F是exe文件，具体参数可自行搜索)
# 5.执行成功后会同目录下会生成build和dist文件夹，打包后的执行程序就在dist目录中，将静态文件如图片，拷贝到dist目录下
# 6.注意，字体要选用系统字体
# 打包exe后执行错误的调试方式，通过命令pyinstaller -D xxxx.py 打包生成一个文件夹，cmd命令进入文件夹执行xxx.exe即可查看错误原因
# 公司打包exe环境目录  E:\pycharm\venv\py37\Scripts