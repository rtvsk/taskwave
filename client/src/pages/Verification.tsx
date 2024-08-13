import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';

import { api } from '../requests/requests';
import { Spinner } from '../components/spinner/Spinner';

export const Verification = () => {
    const { token } = useParams<{ token: string }>();

    useEffect(() => {
        if (!token) {
            return;
        }

        const verificate = async () => {
            try {
                await api.get(`/api/auth/verification/${token}`);
                toast.success(
                    `Вы успешно подвердили свой аккаунт, теперь можете авторизоваться!`
                );
            } catch (err) {
                toast.error('Ошибка при верификации токена');
            }
        };

        verificate();
    }, [token]);

    return <Spinner />;
};
