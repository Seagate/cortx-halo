#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing, please email
# opensource@seagate.com or cortx-questions@seagate.com.

import pytest
from provisioner.components.imagerepo.setup_image_depot import loadImages
from provisioner.components.imagerepo.setup_image_depot import createDir
import os


images = ['calico/kube-controllers', 'calico/cni', 'calico/node', 'k8s.gcr.io/kube-apiserver', 
        'k8s.gcr.io/kube-proxy', 'k8s.gcr.io/kube-controller-manager', 'k8s.gcr.io/kube-scheduler', 
        'k8s.gcr.io/etcd', 'k8s.gcr.io/coredns/coredns']
imagepath = "/opt/halo/install_depot/images"


def test_folderCreation():
    createDir()
    rc1 = os.system("ls %s" %(imagepath))
    assert rc1==0, "/opt/halo/install_depot/images directory not created"


def check_images():
    loadImages()
    for img in images:
        yield img


@pytest.mark.parametrize('img', check_images())
def test_images(img):
    assert os.system("docker images | grep %s" %(img))== 0, "%s is missing" %(img)
