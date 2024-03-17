import { createAsyncThunk } from '@reduxjs/toolkit';

import { api } from '../requests/requests';
import { Token } from '../helpers/helpers';
import {
    TaskGroup,
    taskGroupActions,
} from '../slices/taskGroup/taskGroupSlice';

export const fetchTaskGroups = createAsyncThunk(
    'taskGroups/fetchTaskGroups',
    async (_, { dispatch }): Promise<void> => {
        try {
            const token = Token.get();

            if (!token) {
                return;
            }

            const { data } = await api.get<TaskGroup[]>('/tasks', {
                headers: { Authorization: `Bearer ${token}` },
            });
            dispatch(taskGroupActions.setTaskGroups(data));
        } catch (err) {
            console.error(err);
        }
    }
);
