import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { MeResponse, SigninResponse } from '../../types';
import { userActions } from '../../slices/user/userSlice';

export const signin = createAsyncThunk<
    void,
    { login: string; password: string; history: any }
>('users/signin', async (signinData, { dispatch }): Promise<void> => {
    const { setAuth, setLogin } = userActions;
    try {
        const { history, ...restSigninData } = signinData;

        const {
            data: { access_token },
        } = await api.post<SigninResponse>('/auth/signin', restSigninData);
        const {
            data: { login },
        } = await api.get<MeResponse>('/users/me', {
            headers: { Authorization: `Bearer ${access_token}` },
        });
        dispatch(setAuth(true));
        dispatch(setLogin(login));
        localStorage.setItem('reminderToken', access_token);
        toast(`Успешно!`, {
            type: 'success',
            autoClose: 2000,
            position: 'bottom-right',
        });
        history.push('/tasks');
    } catch (err) {
        toast('Логин/пароль неверные', {
            type: 'error',
            autoClose: 2000,
            position: 'bottom-right',
        });
    }
});
