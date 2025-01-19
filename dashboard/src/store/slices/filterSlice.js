import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { filterService } from '../../services/filter.service';

export const fetchFilters = createAsyncThunk(
  'filters/fetchAll',
  async () => {
    const response = await filterService.getFilters();
    return response;
  }
);

export const createFilter = createAsyncThunk(
  'filters/create',
  async (filter) => {
    const response = await filterService.createFilter(filter);
    return response;
  }
);

export const updateFilter = createAsyncThunk(
  'filters/update',
  async ({ id, updates }) => {
    const response = await filterService.updateFilter(id, updates);
    return response;
  }
);

export const deleteFilter = createAsyncThunk(
  'filters/delete',
  async (id) => {
    await filterService.deleteFilter(id);
    return id;
  }
);

const filterSlice = createSlice({
  name: 'filters',
  initialState: {
    items: [],
    status: 'idle',
    error: null
  },
  reducers: {
    updateFilterStatus: (state, action) => {
      const { id, enabled } = action.payload;
      const filter = state.items.find(f => f.id === id);
      if (filter) {
        filter.enabled = enabled;
      }
    }
  },
  extraReducers: (builder) => {
    builder
      // Fetch filters
      .addCase(fetchFilters.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchFilters.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
        state.error = null;
      })
      .addCase(fetchFilters.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      // Create filter
      .addCase(createFilter.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      // Update filter
      .addCase(updateFilter.fulfilled, (state, action) => {
        const index = state.items.findIndex(f => f.id === action.payload.id);
        if (index !== -1) {
          state.items[index] = action.payload;
        }
      })
      // Delete filter
      .addCase(deleteFilter.fulfilled, (state, action) => {
        state.items = state.items.filter(f => f.id !== action.payload);
      });
  }
});

export const { updateFilterStatus } = filterSlice.actions;
export default filterSlice.reducer; 