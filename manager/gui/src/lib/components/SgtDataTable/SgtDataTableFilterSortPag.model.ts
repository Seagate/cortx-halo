/*
 * CORTX-Halo: Halo Management GUI.
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
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 * For any questions about this software or licensing,
 * please email opensource@seagate.com.
 */

import { SgtFilterObject } from "../SgtChips/SgtFilterObject.model";

export interface SgtDataTableFilterSortPag {
    pagination: PaginationModel;
    filterList: SgtFilterObject[];
    sort: SortModel | null;
}

export interface PaginationModel {
    pageSize: number;
    totalRecords: number;
    currentPage: number;
}

export interface SortModel {
    name: string;
    dir: "asc" | "desc";
}

export interface paginationConfigModel {
    pageLength: number;
    totalVisible: number;
    color?: string;
    nextIcon?: string;
    prevIcon?: string;
    pageSizeList?: { text: string, value: number }[];
}
