import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { FilterRule } from '../types/filter.types';

export const useFilters = () => {
  const [filters, setFilters] = useState<FilterRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFilters = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/filters');
      setFilters(response.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch filters');
    } finally {
      setLoading(false);
    }
  };

  const addFilter = useCallback(async (filter: Omit<FilterRule, 'id'>) => {
    try {
      const response = await axios.post('/api/filters', filter);
      setFilters(prev => [...prev, response.data]);
      return response.data;
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Failed to add filter');
    }
  }, []);

  const updateFilter = useCallback(async (id: string, updates: Partial<FilterRule>) => {
    try {
      const response = await axios.patch(`/api/filters/${id}`, updates);
      setFilters(prev => 
        prev.map(filter => filter.id === id ? response.data : filter)
      );
      return response.data;
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Failed to update filter');
    }
  }, []);

  const deleteFilter = useCallback(async (id: string) => {
    try {
      await axios.delete(`/api/filters/${id}`);
      setFilters(prev => prev.filter(filter => filter.id !== id));
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Failed to delete filter');
    }
  }, []);

  useEffect(() => {
    fetchFilters();
  }, []);

  return {
    filters,
    loading,
    error,
    addFilter,
    updateFilter,
    deleteFilter,
    refreshFilters: fetchFilters
  };
};
