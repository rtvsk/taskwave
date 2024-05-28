import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import {
    ITask,
    WithTaskGroupId,
    taskActions,
} from '../../slices/task/taskSlice';
import { modalActions } from '../../slices/modal/modalSlice';

export const editTask = createAsyncThunk<void, WithTaskGroupId<ITask>>(
    'task/editTask',
    async (
        { id, taskGroupId, title, description = '', deadline },
        thunkApi
    ): Promise<void> => {
        const { dispatch } = thunkApi;

        try {
            const token = Token.get();

            if (!token) {
                return;
            }

            const { data } = await api.patch<Omit<ITask, 'taskGroupId'>>(
                `/api/tasks/${taskGroupId}/task/${id}`,
                { title, description, deadline },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            dispatch(taskActions.updateTask({ ...data, taskGroupId }));

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
            dispatch(modalActions.reset());
        }
    }
);
