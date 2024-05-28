import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { taskActions } from '../../slices/task/taskSlice';

export const deleteTask = createAsyncThunk<
    void,
    { taskGroupId: string; taskId: number }
>(
    'task/deleteTask',
    async ({ taskGroupId, taskId }, { dispatch }): Promise<void> => {
        try {
            const token = Token.get();

            if (!token) {
                return;
            }

            await api.delete(`/api/tasks/${taskGroupId}/task/${taskId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            dispatch(taskActions.deleteTask({ taskGroupId, taskId }));

            toast('deleted', {
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
        }
    }
);
