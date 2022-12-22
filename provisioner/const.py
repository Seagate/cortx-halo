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

from enum import Enum

class FileType(Enum):
    XLSX = 1
    CSV = 2
    INI = 3
    YAML = 4
    JSON = 5

class ResourceType(Enum):
    SERVER_NIC = 1
    SERVER_HBA = 2
    CLUSTER = 3
    SOFTWARE = 4

class SOFTWARE(Enum):
    ANSIBLE = 1
    NODECLI = 2
    K8S_CRI = 3

class PATH(object):
    HALO_BASE_PATH = '/opt/seagate/halo/install_depot/'
    HALOPROV_CFGFILE = './config/haloprov.yaml'
    NODEPREP_CFGFILE = './config/nodeprep.yaml'
    SITE_CFGFILE = './config/sitecfg.yaml'
    RESOURCE_CFGFILE='./{}/config.yaml'
    IMAGE_TAR_FILE_PATH = HALO_BASE_PATH + 'images/'
    ANSIBLE_PATH = HALO_BASE_PATH + 'ansible/'
    K8S_PATH = HALO_BASE_PATH + 'k8s/'
    MINIO_PATH = HALO_BASE_PATH + 'minio/'
    MONITOR_PATH = HALO_BASE_PATH + 'monitor/'
    NODECLI_PATH = HALO_BASE_PATH + 'nodecli/'
    ANSIBLE_INVENTORY_PATH = K8S_PATH + 'inventory.yaml'
    CLUSTER_SETUP_PLAYBOOK_PATH =  K8S_PATH + 'setup_playbook/cluster_setup_playbook.yml'
    CLUSTER_VALIDATE_PLAYBOOK_PATH = K8S_PATH + 'validate_playbook/cluster_validate_playbook.yml'
    LOG_FILE = HALO_BASE_PATH + 'logs/provisioner.log'
    MINIO_FILE_PATH = MINIO_PATH + 'kubectl-minio'
    MINIO_SETUP_PLAYBOOK_PATH = MINIO_PATH + 'setup_playbook/minio_setup_playbook.yml'
    MINIO_VALIDATE_PLAYBOOK_PATH = MINIO_PATH + 'validate_playbook/minio_validate_playbook.yml'
    MINIO_CONFIGURE_PLAYBOOK_PATH = MINIO_PATH + 'configure_playbook/minio_configure_playbook.yml'

class VARIABLE(object):
    IMAGES = ['calico/kube-controllers', 'calico/cni', 'calico/node', 'k8s.gcr.io/kube-apiserver',
        'k8s.gcr.io/kube-proxy', 'k8s.gcr.io/kube-controller-manager', 'k8s.gcr.io/kube-scheduler',
        'k8s.gcr.io/etcd', 'k8s.gcr.io/coredns/coredns']
