import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  Typography,
  Select,
  MenuItem,
  Switch,
  FormControlLabel
} from '@mui/material';

function FilterConfig() {
  const [filters, setFilters] = useState([]);
  const [newFilter, setNewFilter] = useState({
    name: '',
    type: 'text',
    field: '',
    operator: 'equals',
    value: '',
    enabled: true
  });

  useEffect(() => {
    fetchFilters();
  }, []);

  const fetchFilters = async () => {
    try {
      const response = await fetch('/api/filters');
      const data = await response.json();
      setFilters(data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleAddFilter = async () => {
    try {
      const response = await fetch('/api/filters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newFilter),
      });
      
      if (response.ok) {
        fetchFilters();
        setNewFilter({
          name: '',
          type: 'text',
          field: '',
          operator: 'equals',
          value: '',
          enabled: true
        });
      }
    } catch (error) {
      console.error('Error adding filter:', error);
    }
  };

  const handleUpdateFilter = async (id, updates) => {
    try {
      await fetch(`/api/filters/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      });
      fetchFilters();
    } catch (error) {
      console.error('Error updating filter:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>Filter Configuration</Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Add New Filter</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Filter Name"
                    value={newFilter.name}
                    onChange={(e) => setNewFilter({ ...newFilter, name: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Select
                    fullWidth
                    value={newFilter.type}
                    onChange={(e) => setNewFilter({ ...newFilter, type: e.target.value })}
                  >
                    <MenuItem value="text">Text</MenuItem>
                    <MenuItem value="number">Number</MenuItem>
                    <MenuItem value="date">Date</MenuItem>
                  </Select>
                </Grid>
                <Grid item xs={12}>
                  <Button 
                    variant="contained" 
                    onClick={handleAddFilter}
                    disabled={!newFilter.name}
                  >
                    Add Filter
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Active Filters</Typography>
              {filters.map((filter) => (
                <Box key={filter.id} sx={{ mb: 2, p: 2, border: '1px solid #eee' }}>
                  <Grid container alignItems="center" spacing={2}>
                    <Grid item xs={12} sm={4}>
                      <Typography variant="subtitle1">{filter.name}</Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Typography color="textSecondary">
                        {filter.type} | {filter.operator}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={filter.enabled}
                            onChange={(e) => handleUpdateFilter(filter.id, { enabled: e.target.checked })}
                          />
                        }
                        label="Enabled"
                      />
                    </Grid>
                  </Grid>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default FilterConfig;
