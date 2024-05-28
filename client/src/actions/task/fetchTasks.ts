import { createAsyncThunk } from '@reduxjs/toolkit';

import { api } from '../../requests/requests';
import { Token } from '../../helpers/helpers';
import { ITask, taskActions } from '../../slices/task/taskSlice';

export const fetchTasksByTaskGroupId = createAsyncThunk<void, string>(
    'task/fetchTasksByTaskGroupId',
    async (taskGroupId, { dispatch }): Promise<void> => {
        try {
            const token = Token.get();

            if (!token) {
                return;
            }

            const { data } = await api.get<Omit<ITask, 'taskGroupId'>[]>(
                `/api/tasks/${taskGroupId}`,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            const nextTasks: ITask[] = data.map((task) => ({
                ...task,
                taskGroupId: taskGroupId,
            }));

            dispatch(taskActions.addTasks(nextTasks));
        } catch (err) {
            console.error(err);
        }
    }
);
