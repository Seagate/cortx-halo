#! /usr/bin/env python3
import os

def validate():
    try:
        if os.system("ansible --version | grep 2.9.27") != 0:
            return False
        return True
    except Exception as e:
        print(f'{e}')

def main():
    validate()

if __name__ == "__main__":
    main()