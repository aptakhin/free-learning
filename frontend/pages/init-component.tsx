import * as React from 'react';

const initComponent = (name: string, props: object) => {
  const Component = React.lazy(() => import(`./${name}`));
  return <Component {...props} />;
};

export default initComponent;
