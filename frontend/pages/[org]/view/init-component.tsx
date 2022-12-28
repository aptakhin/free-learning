import * as React from 'react';

const initComponent = (name: string, props: object) => {
    console.log('Try load', name, 'and', props)
    const Component = React.lazy(() => import(`${name}`));
    return <Component {...props} />;
    // return <p>{JSON.stringify(props)}</p>
};

export default initComponent;
