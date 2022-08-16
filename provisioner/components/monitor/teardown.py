#! /usr/bin/env python3
import os

def teardown():
    try:
        os.system("yum remove -y monitor")
        return True
    except Exception as e:
        print(f'{e}')
        return False

def main():
    teardown()

if __name__ == "__main__":
    main()