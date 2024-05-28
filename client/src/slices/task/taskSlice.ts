import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface ITask {
    taskGroupId: string;
    id: number;
    title: string;
    description: string | null;
    deadline: string | null;
    is_done: boolean;
}

export type WithTaskGroupId<T> = T & { taskGroupId: string };

interface TaskGroupState {
    tasks: ITask[];
}

const initialState: TaskGroupState = {
    tasks: [],
};

export const TaskSlice = createSlice({
    name: 'taskGroup',
    initialState,
    reducers: {
        addTasks: (state, action: PayloadAction<ITask[]>) => {
            state.tasks = [...state.tasks, ...action.payload];
        },
        addTask: (state, action: PayloadAction<ITask>) => {
            state.tasks = [...state.tasks, action.payload];
        },
        updateTask: (state, action: PayloadAction<ITask>) => {
            const updatedIdx = state.tasks.findIndex(
                (task) =>
                    task.id === action.payload.id &&
                    task.taskGroupId === action.payload.taskGroupId
            );

            if (updatedIdx > -1) {
                state.tasks[updatedIdx].title = action.payload.title;
                state.tasks[updatedIdx].description =
                    action.payload.description;
                state.tasks[updatedIdx].deadline = action.payload.deadline;
                state.tasks[updatedIdx].is_done = action.payload.is_done;
            }
        },
        deleteTask: (
            state,
            action: PayloadAction<{ taskGroupId: string; taskId: number }>
        ) => {
            state.tasks = state.tasks.filter(
                (task) =>
                    !(
                        task.id === action.payload.taskId &&
                        task.taskGroupId === action.payload.taskGroupId
                    )
            );
        },
        deleteAllTasksByTaskGroupId: (
            state,
            action: PayloadAction<{ taskGroupId: string }>
        ) => {
            state.tasks = state.tasks.filter(
                (task) => task.taskGroupId !== action.payload.taskGroupId
            );
        },
        reset: (state) => {
            state.tasks = initialState.tasks;
        },
    },
});

export const taskActions = TaskSlice.actions;

export default TaskSlice.reducer;
