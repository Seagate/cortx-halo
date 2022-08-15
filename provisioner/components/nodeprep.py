#! /usr/bin/env python3
import sys

sys.path.insert(0, '/root/rajnish/cortx-halo')

from provisioner.resource import Software
from common.utils.cmdconfig import *
import os

def main():
    cmdcfg = CmdConfig(FileType.INI,'provisioner/config/nodeprep.cfg')
    for resource in cmdcfg.config_dict.keys():
        swcomp = Software(resource, cmdcfg, None)
        if not swcomp.validate():
            swcomp.setup()
            swcomp.configure()
            swcomp.validate()

if __name__ == "__main__":
    main()