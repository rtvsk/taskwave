import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';

import { userActions } from '../slices/user/userSlice';
import { globalActions } from '../slices/global/globalSlice';
import { api } from '../requests/requests';
import { MeResponse } from '../types';
import { Token } from '../helpers/helpers';

export const useInitial = () => {
    const history = useHistory();
    const dispatch = useDispatch();

    const { setAuth, setLogin } = userActions;
    const { setIsLoading } = globalActions;

    const resetUserAndGoSignin = () => {
        dispatch(setAuth(false));
        dispatch(setLogin(null));
        dispatch(setIsLoading(false));
        history.push('/sign-in');
    };

    useEffect(() => {
        const checkWhoAmI = async () => {
            await new Promise((resolve) => setTimeout(resolve, 1000));

            const token = Token.get();

            if (!token) {
                resetUserAndGoSignin();

                return;
            }

            try {
                const {
                    data: { login },
                } = await api.get<MeResponse>('/api/users/me', {
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (login) {
                    dispatch(setAuth(true));
                    dispatch(setLogin(login));
                    dispatch(setIsLoading(false));
                    history.push('/tasks');
                }
            } catch (err) {
                dispatch(setAuth(false));
                dispatch(setLogin(null));
                dispatch(setIsLoading(false));
                history.push('/sign-in');
                Token.delete();
            }
        };

        checkWhoAmI();
    }, [history, dispatch]);
};
