#! /usr/bin/env python3
import os

hostname = "ssc-vm-g2-rhev4-3413"
src_path = "/root/packages/k8s"
work_dir ="/root/k8s"

def mountNFS():
    os.system("mount %s:%s %s" %(hostname, src_path, work_dir))

def pullNFS():
    os.system("cp * /opt/halo/install_depot")

def main():
    mountNFS()
    pullNFS()

if __name__ == "__main__":
    main()