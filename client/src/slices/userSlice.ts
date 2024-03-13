import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface UserState {
    isAuthed: boolean;
}

const initialState: UserState = {
    isAuthed: false,
};

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setAuth: (state, action: PayloadAction<boolean>) => {
            state.isAuthed = action.payload;
        },
    },
});

// Action creators are generated for each case reducer function
export const { setAuth } = userSlice.actions;

export default userSlice.reducer;
