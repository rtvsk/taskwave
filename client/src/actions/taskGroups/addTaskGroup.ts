import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { taskGroupActions } from '../../slices/taskGroup/taskGroupSlice';
import { modalActions } from '../../slices/modal/modalSlice';

export const addTaskGroup = createAsyncThunk<
    void,
    { title: string; description: string; deadline: string | null }
>('taskGroup/add', async (taskGroupData, { dispatch }): Promise<void> => {
    try {
        dispatch(taskGroupActions.setIsLoading(true));
        const token = Token.get();

        if (!token) {
            return;
        }

        const {
            data: { id, title, description, deadline },
        } = await api.post('/api/tasks', taskGroupData, {
            headers: { Authorization: `Bearer ${token}` },
        });

        dispatch(
            taskGroupActions.addTaskGroup({ id, title, description, deadline })
        );
        toast('Woohoooo!', {
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
});
