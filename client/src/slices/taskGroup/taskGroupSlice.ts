import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface TaskGroupState {
    isLoading: boolean;
}

const initialState: TaskGroupState = {
    isLoading: false,
};

export const TaskGroupSlice = createSlice({
    name: 'taskGroup',
    initialState,
    reducers: {
        setIsLoading: (state, action: PayloadAction<boolean>) => {
            state.isLoading = action.payload;
        },
    },
});

export const taskGroupActions = TaskGroupSlice.actions;

export default TaskGroupSlice.reducer;
