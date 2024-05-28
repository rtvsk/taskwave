import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { taskGroupActions } from '../../slices/taskGroup/taskGroupSlice';
import { modalActions } from '../../slices/modal/modalSlice';

export const editTaskGroup = createAsyncThunk<
    void,
    {
        id: string;
        title: string;
        description: string | null;
        deadline: string | null;
    }
>(
    'taskGroup/edit',
    async (
        { id, title, description = '', deadline },
        thunkApi
    ): Promise<void> => {
        const { dispatch } = thunkApi;

        try {
            dispatch(taskGroupActions.setIsLoading(true));
            const token = Token.get();

            if (!token) {
                return;
            }

            await api.patch(
                `/api/tasks/${id}`,
                { title, description, deadline },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            dispatch(
                taskGroupActions.updateTaskGroup({
                    id,
                    title,
                    description,
                    deadline,
                })
            );

            toast('editted!', {
                type: 'success',
                autoClose: 2000,
                position: 'bottom-right',
            });
        } catch (err) {
            toast('Something went wrong :(', {
                type: 'error',
                autoClose: 2000,
                position: 'bottom-right',
            });
        } finally {
            dispatch(taskGroupActions.setIsLoading(false));
            dispatch(modalActions.reset());
        }
    }
);
