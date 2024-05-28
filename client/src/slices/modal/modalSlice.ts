import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface ModalState<T> {
    name: string | null;
    data: null | T;
}

const initialState: ModalState<any> = {
    name: null,
    data: null,
};

export const modalSlice = createSlice({
    name: 'modal',
    initialState,
    reducers: {
        set: (state, action: PayloadAction<ModalState<any>>) => {
            state.name = action.payload.name;
            state.data = action.payload.data;
        },
        reset: (state) => {
            state.name = initialState.name;
            state.data = initialState.data;
        },
    },
});

export const modalActions = modalSlice.actions;

export default modalSlice.reducer;
