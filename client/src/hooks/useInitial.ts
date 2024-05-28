import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';

import { userActions } from '../slices/user/userSlice';
import { globalActions } from '../slices/global/globalSlice';
import { api } from '../requests/requests';
import { MeResponse } from '../types';
import { Token } from '../helpers/helpers';
import { taskActions } from '../slices/task/taskSlice';
import { taskGroupActions } from '../slices/taskGroup/taskGroupSlice';

export const useInitial = () => {
    const history = useHistory();
    const dispatch = useDispatch();

    const { setIsLoading } = globalActions;

    const resetUserAndGoSignin = () => {
        dispatch(userActions.logout());
        dispatch(taskActions.reset());
        dispatch(taskGroupActions.reset());
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
                const { data } = await api.get<MeResponse>('/api/users/me', {
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (data) {
                    dispatch(userActions.setUser(data));
                    dispatch(setIsLoading(false));
                    history.push('/tasks');
                }
            } catch (err) {
                dispatch(userActions.logout());
                dispatch(taskActions.reset());
                dispatch(taskGroupActions.reset());
                dispatch(setIsLoading(false));
                history.push('/sign-in');
                Token.delete();
            }
        };

        checkWhoAmI();
    }, [history, dispatch]);
};
