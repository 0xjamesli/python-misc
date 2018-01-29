import sys,os
name = input()
print(os.system('netsh wlan show profile name=' + name + ' key=clear'))
input()
