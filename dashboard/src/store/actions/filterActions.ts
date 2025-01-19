import { createAsyncThunk } from '@reduxjs/toolkit';
import { filterService } from '../../services/filter.service';
import { FilterRule } from '../../types/filter.types';

export const fetchFilters = createAsyncThunk(
  'filters/fetchAll',
  async () => {
    const filters = await filterService.getFilters();
    return filters;
  }
);

export const createFilter = createAsyncThunk(
  'filters/create',
  async (filter: Omit<FilterRule, 'id'>) => {
    const newFilter = await filterService.createFilter(filter);
    return newFilter;
  }
);

export const updateFilter = createAsyncThunk(
  'filters/update',
  async ({ id, updates }: { id: string; updates: Partial<FilterRule> }) => {
    const updatedFilter = await filterService.updateFilter(id, updates);
    return updatedFilter;
  }
);

export const deleteFilter = createAsyncThunk(
  'filters/delete',
  async (id: string) => {
    await filterService.deleteFilter(id);
    return id;
  }
);

export const testFilter = createAsyncThunk(
  'filters/test',
  async (filter: FilterRule) => {
    const results = await filterService.testFilter(filter);
    return { filter, results };
  }
);
