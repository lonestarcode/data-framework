import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { createStore } from '../../store/store';
import { FilterBuilder } from '../../components/FilterBuilder';
import { filterService } from '../../services/filter.service';
import { FilterType, FilterOperator, FilterRule } from '../../types/filter.types';
import userEvent from '@testing-library/user-event';

jest.mock('../../services/filter.service');

describe('FilterBuilder Unit Tests', () => {
  let store: ReturnType<typeof createStore>;

  const mockFilter: FilterRule = {
    id: '1',
    name: 'Test Filter',
    type: FilterType.TEXT,
    field: 'content',
    operator: FilterOperator.CONTAINS,
    value: 'test',
    enabled: true,
    priority: 1,
    category: 'advisory'
  };

  beforeEach(() => {
    store = createStore();
    jest.clearAllMocks();
    setupMocks();
  });

  const setupMocks = () => {
    (filterService.testFilter as jest.Mock).mockResolvedValue({
      passRate: 0.85,
      sampleSize: 100,
      processingTime: 150,
      examples: {
        passed: ['Example 1', 'Example 2'],
        failed: ['Example 3']
      }
    });
  };

  const renderComponent = (props = {}) => {
    return render(
      <Provider store={store}>
        <FilterBuilder {...props} />
      </Provider>
    );
  };

  test('renders filter builder form', () => {
    renderComponent();

    expect(screen.getByLabelText(/filter name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/field/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/operator/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/value/i)).toBeInTheDocument();
  });

  test('creates new filter with basic configuration', async () => {
    renderComponent();

    // Fill form
    await userEvent.type(screen.getByLabelText(/filter name/i), 'New Filter');
    await userEvent.type(screen.getByLabelText(/field/i), 'content');
    await userEvent.selectOptions(screen.getByLabelText(/type/i), FilterType.TEXT);
    await userEvent.selectOptions(screen.getByLabelText(/operator/i), FilterOperator.CONTAINS);
    await userEvent.type(screen.getByLabelText(/value/i), 'test value');

    // Save filter
    fireEvent.click(screen.getByTestId('save-filter'));

    await waitFor(() => {
      expect(filterService.createFilter).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'New Filter',
          field: 'content',
          type: FilterType.TEXT,
          operator: FilterOperator.CONTAINS,
          value: 'test value'
        })
      );
    });
  });

  test('validates required fields', async () => {
    renderComponent();

    // Try to save without required fields
    fireEvent.click(screen.getByTestId('save-filter'));

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/field is required/i)).toBeInTheDocument();
      expect(screen.getByText(/value is required/i)).toBeInTheDocument();
    });
  });

  test('handles filter testing', async () => {
    renderComponent();

    // Fill required fields
    await userEvent.type(screen.getByLabelText(/filter name/i), 'Test Filter');
    await userEvent.type(screen.getByLabelText(/field/i), 'content');
    await userEvent.selectOptions(screen.getByLabelText(/type/i), FilterType.TEXT);
    await userEvent.selectOptions(screen.getByLabelText(/operator/i), FilterOperator.CONTAINS);
    await userEvent.type(screen.getByLabelText(/value/i), 'test');

    // Test filter
    fireEvent.click(screen.getByTestId('test-filter'));

    await waitFor(() => {
      expect(screen.getByText('85%')).toBeInTheDocument(); // Pass rate
      expect(screen.getByText('100')).toBeInTheDocument(); // Sample size
      expect(screen.getByText('150ms')).toBeInTheDocument(); // Processing time
    });
  });

  test('loads and edits existing filter', async () => {
    renderComponent({ filter: mockFilter });

    // Verify form is pre-filled
    expect(screen.getByLabelText(/filter name/i)).toHaveValue(mockFilter.name);
    expect(screen.getByLabelText(/field/i)).toHaveValue(mockFilter.field);
    expect(screen.getByLabelText(/type/i)).toHaveValue(mockFilter.type);

    // Make changes
    await userEvent.clear(screen.getByLabelText(/filter name/i));
    await userEvent.type(screen.getByLabelText(/filter name/i), 'Updated Filter');

    // Save changes
    fireEvent.click(screen.getByTestId('save-filter'));

    await waitFor(() => {
      expect(filterService.updateFilter).toHaveBeenCalledWith(
        mockFilter.id,
        expect.objectContaining({
          name: 'Updated Filter'
        })
      );
    });
  });

  test('handles advanced filter options', async () => {
    renderComponent();

    // Open advanced options
    fireEvent.click(screen.getByText(/advanced options/i));

    // Set priority
    await userEvent.type(screen.getByLabelText(/priority/i), '2');

    // Set category
    await userEvent.selectOptions(screen.getByLabelText(/category/i), 'prohibitive');

    // Add description
    await userEvent.type(
      screen.getByLabelText(/description/i),
      'Test filter description'
    );

    // Save filter
    fireEvent.click(screen.getByTestId('save-filter'));

    await waitFor(() => {
      expect(filterService.createFilter).toHaveBeenCalledWith(
        expect.objectContaining({
          priority: 2,
          category: 'prohibitive',
          description: 'Test filter description'
        })
      );
    });
  });

  test('handles operator-specific value inputs', async () => {
    renderComponent();

    // Select number type
    await userEvent.selectOptions(screen.getByLabelText(/type/i), FilterType.NUMBER);

    // Select between operator
    await userEvent.selectOptions(screen.getByLabelText(/operator/i), FilterOperator.BETWEEN);

    // Verify range inputs appear
    expect(screen.getByLabelText(/minimum value/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/maximum value/i)).toBeInTheDocument();

    // Enter range values
    await userEvent.type(screen.getByLabelText(/minimum value/i), '10');
    await userEvent.type(screen.getByLabelText(/maximum value/i), '20');

    // Save filter
    fireEvent.click(screen.getByTestId('save-filter'));

    await waitFor(() => {
      expect(filterService.createFilter).toHaveBeenCalledWith(
        expect.objectContaining({
          value: [10, 20]
        })
      );
    });
  });
});
