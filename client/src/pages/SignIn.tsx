import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { ThemeProvider } from '@mui/material/styles';
import { useHistory } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import { LinkBehavior } from '../components/LinkBehavior';
import { theme } from '../theme/theme';
import { signin } from '../components/actions/signin';

function Copyright(props: any) {
    return (
        <Typography
            variant='body2'
            color='text.secondary'
            align='center'
            {...props}
        >
            {'Copyright © '}
            <Link color='inherit' href='https://mui.com/'>
                Reminder.su
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

// TODO remove, this demo shouldn't need to reset the theme.
// const defaultTheme = createTheme();

export const SignIn = () => {
    // const { isAuthed, id: userId } = useSelector(
    //     (state: RootState) => state.user
    // );
    const dispatch = useDispatch();

    const history = useHistory();

    const handleSubmit = React.useCallback(
        async (event: React.FormEvent<HTMLFormElement>) => {
            event.preventDefault();
            const data = new FormData(event.currentTarget);
            const signinData = {
                login: String(data.get('login')),
                password: String(data.get('password')),
            };
            dispatch(signin({ ...signinData, history }) as any);

            // try {
            //     const {
            //         data: { access_token },
            //     } = await api.post<SigninResponse>('/auth/signin', signinData);
            //     const {
            //         data: { login },
            //     } = await api.get<MeResponse>('/users/me', {
            //         headers: { Authorization: `Bearer ${access_token}` },
            //     });
            //     dispatch(setAuth(true));
            //     dispatch(setLogin(login));
            //     localStorage.setItem('reminderToken', access_token);
            //     toast(`Успешно!`, {
            //         type: 'success',
            //         autoClose: 2000,
            //         position: 'bottom-right',
            //     });
            //     history.push('/tasks');
            // } catch (err) {
            //     toast('Логин/пароль неверные', {
            //         type: 'error',
            //         autoClose: 2000,
            //         position: 'bottom-right',
            //     });
            // }
            // dispatch(userSignIn({ ...signinData, history }));
        },
        []
    );

    return (
        <ThemeProvider theme={theme}>
            <Container component='main' maxWidth='xs'>
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component='h1' variant='h5'>
                        Войти
                    </Typography>
                    <Box
                        component='form'
                        onSubmit={handleSubmit}
                        noValidate
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin='normal'
                            required
                            fullWidth
                            id='login'
                            label='Login'
                            name='login'
                            autoComplete='login'
                            autoFocus
                        />
                        <TextField
                            margin='normal'
                            required
                            fullWidth
                            name='password'
                            label='Password'
                            type='password'
                            id='password'
                            autoComplete='current-password'
                        />
                        <FormControlLabel
                            control={
                                <Checkbox value='remember' color='primary' />
                            }
                            label='Запомнить меня'
                        />
                        <Button
                            type='submit'
                            fullWidth
                            variant='contained'
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Войти
                        </Button>
                        <Grid container>
                            <Grid item xs>
                                <Link href='#' variant='body2'>
                                    Забыли пароль?
                                </Link>
                            </Grid>
                            <Grid item>
                                <Link
                                    href='/sign-up'
                                    variant='body2'
                                    component={LinkBehavior}
                                    onClick={() => {}}
                                >
                                    {'Зарегистрироваться'}
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
                <Copyright sx={{ mt: 8, mb: 4 }} />
            </Container>
        </ThemeProvider>
    );
};
