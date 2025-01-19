import { useEffect } from 'react';
import { useActions, useAppSelector } from './useRedux';
import { wsService } from '../services/websocket.service';

export const useFilters = () => {
  const { filters } = useActions();
  const filterItems = useAppSelector(state => state.filters.items);
  const status = useAppSelector(state => state.filters.status);
  const error = useAppSelector(state => state.filters.error);

  useEffect(() => {
    filters.fetchFilters();

    const unsubscribe = wsService.subscribe('filter_update', (data) => {
      filters.fetchFilters(); // Refresh filters when update received
    });

    return () => unsubscribe();
  }, []);

  return {
    filters: filterItems,
    status,
    error,
    createFilter: filters.createFilter,
    updateFilter: filters.updateFilter,
    deleteFilter: filters.deleteFilter,
    refreshFilters: filters.fetchFilters
  };
}; 