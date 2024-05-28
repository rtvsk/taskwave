import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from 'react-toastify';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { modalActions } from '../../slices/modal/modalSlice';
import { taskActions } from '../../slices/task/taskSlice';

export const addTask = createAsyncThunk<
    void,
    {
        taskGroupId: string;
        title: string;
        description: string;
        deadline: string | null;
    }
>('task/addTask', async (rawTaskData, { dispatch }): Promise<void> => {
    try {
        const token = Token.get();

        if (!token) {
            return;
        }

        const { taskGroupId, ...restTaskData } = rawTaskData;

        const {
            data: { id, title, description, deadline, is_done },
        } = await api.post(`/api/tasks/${taskGroupId}`, restTaskData, {
            headers: { Authorization: `Bearer ${token}` },
        });

        dispatch(
            taskActions.addTask({
                id,
                title,
                description,
                deadline,
                taskGroupId,
                is_done,
            })
        );
        // dispatch(fetchTasksByTaskGroupId(taskGroupId));
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
        dispatch(modalActions.reset());
    }
});
