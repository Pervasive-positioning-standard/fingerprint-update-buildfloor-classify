# fingerprint-update-buildfloor-classify
Four .py files +two datasets +one introduce markdown
please put them together in the zip
1. alter_ap data pre.py in model3-server
2. modelfitchange.py in model3-server
3.fingerprint.text in model3-server
4. mac1.py in platform-web-API--main
5.classify.py in platform-web-API--main
6.wifiscanner.dat in platform-web-API--main

Introduce how to run these python file:

1: open the alter_ap data pre.py in model3-server and run it(here, I just use 1F to do example and update the 1F fingerprint)
   to make pandas of alter_ap and it will use the modelfitchange.py to do the GP model and update the fingerprint by itself.
 
2. classify
   open the mac1.py and run it to make pandas about the mac position in mango and this will produce one csv.file
   open the classify.py and run it, which can read csv.file and make pandas about usersignal, then do classify for usersignal and return the pandas about      userid/build/floor for users.

