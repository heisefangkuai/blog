# python常见问题

## 报错1

ModuleNotFoundError: No module named 'pip'

可以首先执行  python -m ensurepip  然后执行 python -m pip install --upgrade pip  即可更新完毕。

## 报错1

ModuleNotFoundError: No module named 'pip._internal.cli'
强制重新安装
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
