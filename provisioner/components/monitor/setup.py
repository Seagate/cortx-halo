#! /usr/bin/env python3
import os

filename = "/opt/halo/install_depot/monitor.tar.gz"
extract_path = "/opt/halo/install_depot/k8s"

def createFile():
    try:
        if os.system("ls %s" %(extract_path)) != 0:
            os.system("mkdir %s" %(extract_path))
    except Exception as e:
        print(f'{e}')

def setup():
    try:
        os.chdir("%s" %(extract_path))
        os.system("tar xvf %s -C %s" %(filename, extract_path))
        os.system("yum localinstall -y *.rpm")
    except Exception as e:
        print(f'{e}')

def main():
    createFile()
    setup()

if __name__ == "__main__":
    main()