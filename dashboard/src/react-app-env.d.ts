/// <reference types="react-scripts" />

declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
    REACT_APP_API_URL: string;
    REACT_APP_WS_URL: string;
    REACT_APP_VERSION: string;
    REACT_APP_BUILD_TIME: string;
  }
}

declare module '*.svg' {
  import * as React from 'react';
  export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  const src: string;
  export default src;
}

declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.sass' {
  const classes: { [key: string]: string };
  export default classes;
}

// Add custom type definitions for any third-party modules that don't have TypeScript definitions
declare module 'some-untyped-module' {
  const content: any;
  export default content;
}

interface Window {
  // Add any custom window properties here
  __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: any;
}
