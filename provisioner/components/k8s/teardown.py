#! /usr/bin/env python3
import os

def teardown():
    try:
        os.system("yum remove -y kubectl kubeadm kubelet")
    except Exception as e:
        print(f'{e}')

def main():
    teardown()

if __name__ == "__main__":
    main()