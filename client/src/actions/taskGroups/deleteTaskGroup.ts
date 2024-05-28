import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { taskGroupActions } from '../../slices/taskGroup/taskGroupSlice';
import { taskActions } from '../../slices/task/taskSlice';

export const deleteTaskGroup = createAsyncThunk<void, string>(
    'taskGroup/delete',
    async (id, thunkApi): Promise<void> => {
        const { dispatch } = thunkApi;
        try {
            dispatch(taskGroupActions.setIsLoading(true));
            const token = Token.get();

            if (!token) {
                return;
            }

            await api.delete(`/api/tasks/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            dispatch(taskGroupActions.deleteTaskGroup(id));
            dispatch(
                taskActions.deleteAllTasksByTaskGroupId({ taskGroupId: id })
            );

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
        } finally {
            dispatch(taskGroupActions.setIsLoading(false));
        }
    }
);
