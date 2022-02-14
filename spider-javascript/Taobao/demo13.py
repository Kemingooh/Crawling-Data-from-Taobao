import os
shop_name = '123'
shop_shell = "adb shell am broadcast -a ADB_INPUT_TEXT --es msg '{}'".format(shop_name)
os.system(shop_shell)