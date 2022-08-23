import { graphImages } from '../health/LrHeathGraphImages.constant';

/*
 * CORTX-CSM: CORTX Management web.
 * Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see https://www.gnu.org/licenses/.
 * For any questions about this software or licensing,
 * please email opensource@seagate.com.
 */
export const dashboardCardData = {
  storageComponents: [
    {
      title: 0,
      description: "buckets",
      imgUrl: "storage-buckets.svg",
      navPath: "",
    },
    {
      title: 0,
      description: "objects",
      imgUrl: "storage-objects.svg",
      navPath: "",
    },
    {
      title: 0,
      description: "underReplicated",
      imgUrl: "storage-under-replicated.svg",
      navPath: "",
    },
    {
      title: 0,
      description: "S3 Account",
      imgUrl: "storage-profile.svg",
      navPath: "",
    },
    {
      title: 0,
      description: "IAM User",
      imgUrl: "storage-profile.svg",
      navPath: "",
    },
    {
      title: 0,
      description: "Tenants",
      imgUrl: "storage-profile.svg",
      navPath: "",
    },
  ],
  performance: [
    {
      imgUrl: "performance-read-throughput-good.svg",
      imgUrl2: "performance-read-graph.svg",
      navPath: "/performance",
      count: 0,
      unit: "Gbps",
      title: "readThroughput",
    },
    {
      imgUrl: "performance-write-throughput-good.svg",
      imgUrl2: "performance-write-graph.svg",
      navPath: "/performance",
      count: 0,
      unit: "Gbps",
      title: "writeThroughput",
    }
  ],
  clusterNodes: [
    {
      count: 0,
      unit: "nodes",
      title: "online",
      imgUrl: "health-online-nodes.svg",
      color: "#E2F2DB"
    },
    {
      count: 0,
      unit: "nodes",
      title: "offline",
      imgUrl: "health-offline-nodes.svg",
      color: "#EEEEEE"
    },
    {
      count: 0,
      unit: "nodes",
      title: "failed",
      imgUrl: "health-failed-nodes.svg",
      color: "#FBE9EA"
    },
    {
      count: 0,
      unit: "nodes",
      title: "degraded",
      imgUrl: "health-degraded-nodes.svg",
      color: "#FDEDD4"
    },
  ],
  alerts: [
    {
      title: 0,
      description: "fatal",
      imgUrl: "alert-fatal.svg",
    },
    {
      title: 0,
      description: "critical",
      imgUrl: "alert-critical.svg",
    },
    {
      title: 0,
      description: "error",
      imgUrl: "alert-error.svg",
    },
    {
      title: 0,
      description: "warning",
      imgUrl: "alert-warning.svg",
    },
    {
      title: 0,
      description: "informational",
      imgUrl: "alert-informational.svg",
    },
  ],
  bgActivities: [
    {
      title: 0,
      description: "tasks",
      imgUrl: "bg-tasks.svg",
      navPath: "",
    },
  ],
  clusterHealth: {
    online: {
      color: "#E2F2DB",
      image: "health-online-cluster.svg"
    },
    offline: {
      color: "#EEEEEE",
      image: "health-offline-cluster.svg"
    },
    degraded: {
      color: "#FDEDD4",
      image: "health-degraded-cluster.svg"
    },
    failed: {
      color: "#FBE9EA",
      image: "health-failed-cluster.svg"
    }
  }
};
