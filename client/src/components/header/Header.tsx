import { Avatar, Box, IconButton, Typography } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { useMemo } from 'react';
import LogoutIcon from '@mui/icons-material/Logout';
import { useHistory } from 'react-router-dom';
import { toast } from 'react-toastify';

import { isAuthedSelector, loginSelector } from '../../slices/user/selectors';
import { userActions } from '../../slices/user/userSlice';

export const Header = () => {
    const isAuthed = useSelector(isAuthedSelector);
    const login = useSelector(loginSelector);
    const history = useHistory();
    const dispatch = useDispatch();
    const { setAuth, setLogin } = userActions;

    const onLogout = () => {
        history.push('/sign-in');
        dispatch(setAuth(false));
        dispatch(setLogin(null));
        localStorage.removeItem('reminderToken');
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
                <Avatar sx={{ width: 24, height: 24 }}>
                    {login.charAt(0)}
                </Avatar>
                <Typography component='h1' variant='h6'>
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
                        Reminder.su
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
