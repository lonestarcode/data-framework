
# Analytics Dashboard Frontend

A modern React-based analytics dashboard for monitoring and managing data filtering operations.

## Features

- 📊 Real-time analytics visualization
- 🔍 Advanced filter configuration
- 💬 Interactive chat interface
- 📈 Time-series data analysis
- 🔄 Real-time WebSocket updates
- 🎨 Responsive design
- 🌙 Dark/Light theme support

## Tech Stack

- React 18
- TypeScript
- Redux Toolkit
- React Router
- WebSocket
- Jest & Testing Library
- CSS Modules

## Project Structure

```
dashboard/
├── src/
│   ├── components/     # React components
│   ├── store/         # Redux store configuration
│   │   ├── slices/    # Redux slices
│   │   └── store.ts   # Store configuration
│   ├── services/      # API services
│   ├── types/         # TypeScript types
│   ├── utils/         # Utility functions
│   └── tests/         # Test files
│       ├── unit/      # Unit tests
│       └── integration/# Integration tests
```

## Getting Started

### Prerequisites

- Node.js (v16+)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-repo/dashboard.git
cd dashboard
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env` file:
```env
REACT_APP_API_URL=http://localhost:8080/api
REACT_APP_WS_URL=ws://localhost:8080/ws
```

4. Start the development server:
```bash
npm start
# or
yarn start
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run lint` - Runs ESLint
- `npm run format` - Formats code with Prettier

## Testing

The project uses Jest and React Testing Library for testing. Tests are organized into:

- Unit tests (`/tests/unit/`)
- Integration tests (`/tests/integration/`)

Run tests with:
```bash
npm test
# or
yarn test
```

## Code Style

- ESLint for code linting
- Prettier for code formatting
- TypeScript for type safety

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| REACT_APP_API_URL | Backend API URL | http://localhost:8080/api |
| REACT_APP_WS_URL | WebSocket URL | ws://localhost:8080/ws |
| REACT_APP_VERSION | App version | - |
| REACT_APP_BUILD_TIME | Build timestamp | - |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Component Documentation

### AnalyticsView
Main analytics dashboard component displaying metrics and charts.

### FilterBuilder
Component for creating and editing data filters with real-time testing.

### ChatInterface
Interactive chat interface with message history and real-time updates.

## State Management

Redux Toolkit is used for state management with the following slices:
- Analytics: Manages analytics data and metrics
- Filters: Handles filter configurations
- Chat: Manages chat messages and sessions

## API Integration

- RESTful API calls using Axios
- Real-time updates via WebSocket
- Error handling and retry mechanisms
- Request/response interceptors

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Optimization

- Code splitting
- Lazy loading
- Memoization
- WebSocket connection management
- Efficient re-rendering strategies

