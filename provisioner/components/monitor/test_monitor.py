from setup import *
from teardown import *
from validate import *


def test_folderCreation():
    createFile()
    x = os.system("ls /opt/halo/install_depot/monitor")
    print(x)
    assert x==0, "File not created"

def test_setup():
    setup()
    x = validate()
    assert x!=0, "Software not installed"

def test_teardown():
    x = teardown()
    assert x!=0, "Teardown Failed"