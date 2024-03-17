import React from 'react';
import Box from '@mui/material/Box';

interface Props {}

const withContainerWrapper = (WrappedComponent: React.ComponentType<Props>) => {
    return function HeaderBoxWrapper(props: Props) {
        return (
            <Box
                component={'section'}
                width={'100%'}
                maxWidth={'100%'}
                marginLeft={'auto'}
                marginRight={'auto'}
                display={'flex'}
                justifyContent={'center'}
                paddingInline={'16px'}
                id='container'
            >
                <Box width={'100%'} maxWidth={'976px'}>
                    <WrappedComponent {...props} />
                </Box>
            </Box>
        );
    };
};

export default withContainerWrapper;
