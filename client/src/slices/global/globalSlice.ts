import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface GlobalState {
    isLoading: boolean;
}

const initialState: GlobalState = {
    isLoading: true,
};

export const globalSlice = createSlice({
    name: 'global',
    initialState,
    reducers: {
        setIsLoading: (state, action: PayloadAction<boolean>) => {
            state.isLoading = action.payload;
        },
    },
});

export const globalActions = globalSlice.actions;

export default globalSlice.reducer;
