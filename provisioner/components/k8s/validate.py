#! /usr/bin/env python3
import os

def validate():
    try:
        if os.system("kubctl --version | grep 1.24.3") != 0:
            print("Version Mismatch")
    except Exception as e:
        print(f'{e}')

def main():
    validate()

if __name__ == "__main__":
    main()