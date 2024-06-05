import { Box, IconButton, Typography } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { useMemo } from 'react';
import LogoutIcon from '@mui/icons-material/Logout';
import { useHistory } from 'react-router-dom';
import { toast } from 'react-toastify';

import { isAuthedSelector, loginSelector } from '../../slices/user/selectors';
import { userActions } from '../../slices/user/userSlice';
import { Token } from '../../helpers/helpers';
import { taskActions } from '../../slices/task/taskSlice';
import { taskGroupActions } from '../../slices/taskGroup/taskGroupSlice';

export const Header = () => {
    const isAuthed = useSelector(isAuthedSelector);
    const login = useSelector(loginSelector);
    const history = useHistory();
    const dispatch = useDispatch();

    const onLogout = () => {
        history.push('/sign-in');
        dispatch(userActions.logout());
        dispatch(taskActions.reset());
        dispatch(taskGroupActions.reset());
        Token.delete();
        toast(`Вы вышли из приложения`, {
            type: 'info',
            autoClose: 2000,
            position: 'bottom-right',
        });
    };

    const loginSection = useMemo(() => {
        if (!login || !isAuthed) {
            return null;
        }

        return (
            <>
                <Typography component='span' variant='subtitle1'>
                    {login}
                </Typography>
                <IconButton size='small' onClick={onLogout}>
                    <LogoutIcon color='error' />
                </IconButton>
            </>
        );
    }, [login, isAuthed]);

    return (
        <Box
            component={'header'}
            height={52}
            width={'100%'}
            maxWidth={'100%'}
            marginLeft={'auto'}
            marginRight={'auto'}
            display={'flex'}
            justifyContent={'center'}
            paddingInline={'16px'}
            borderBottom={'rgba(0, 0, 0, 0.23) 1px solid'}
            id='header'
        >
            <Box
                display={'flex'}
                alignItems={'center'}
                justifyContent={'space-between'}
                width={'100%'}
                maxWidth={'976px'}
            >
                <Box maxWidth={'200px'}>
                    <Typography component='h1' variant='h6'>
                        Taskwave.ru
                    </Typography>
                </Box>
                <Box
                    maxWidth={'200px'}
                    display={'flex'}
                    justifyContent={'flex-end'}
                    alignItems={'center'}
                    gap={'12px'}
                >
                    {loginSection}
                </Box>
            </Box>
        </Box>
    );
};
