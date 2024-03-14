import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface UserState {
    isAuthed: boolean;
    login: string | null;
}

const initialState: UserState = {
    isAuthed: false,
    login: null,
};

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setAuth: (state, action: PayloadAction<boolean>) => {
            state.isAuthed = action.payload;
        },
        setLogin: (state, action: PayloadAction<UserState['login']>) => {
            state.login = action.payload;
        },
    },
});

export const userActions = userSlice.actions;

export default userSlice.reducer;
