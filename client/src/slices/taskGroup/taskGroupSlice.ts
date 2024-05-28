import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface ITaskGroup {
    title: string;
    description: string | null;
    id: string;
    deadline: string | null;
}

interface TaskGroupState {
    taskGroups: ITaskGroup[];
    isLoading: boolean;
}

const initialState: TaskGroupState = {
    isLoading: false,
    taskGroups: [],
};

export const TaskGroupSlice = createSlice({
    name: 'taskGroup',
    initialState,
    reducers: {
        setIsLoading: (state, action: PayloadAction<boolean>) => {
            state.isLoading = action.payload;
        },
        setTaskGroups: (state, action: PayloadAction<ITaskGroup[]>) => {
            state.taskGroups = action.payload;
        },
        updateTaskGroup: (state, action: PayloadAction<ITaskGroup>) => {
            const updatedIdx = state.taskGroups.findIndex(
                (tg) => tg.id === action.payload.id
            );

            if (updatedIdx > -1) {
                state.taskGroups[updatedIdx].title = action.payload.title;
                state.taskGroups[updatedIdx].description =
                    action.payload.description;
                state.taskGroups[updatedIdx].deadline = action.payload.deadline;
            }
            // state.taskGroups = action.payload;
        },
        deleteTaskGroup: (state, action: PayloadAction<ITaskGroup['id']>) => {
            const filteredTaskGroups = state.taskGroups.filter(
                (tg) => tg.id !== action.payload
            );

            state.taskGroups = filteredTaskGroups;
        },
        addTaskGroup: (state, action: PayloadAction<ITaskGroup>) => {
            state.taskGroups = [...state.taskGroups, action.payload];
        },
        reset: (state) => {
            state.taskGroups = initialState.taskGroups;
            state.isLoading = initialState.isLoading;
        },
    },
});

export const taskGroupActions = TaskGroupSlice.actions;

export default TaskGroupSlice.reducer;
