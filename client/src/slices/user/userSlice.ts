import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface UserState {
    isAuthed: boolean;
    login: string | null;
    email: string | null;
    firstname: string | null;
    lastname: string | null;
}

const initialState: UserState = {
    isAuthed: false,
    login: null,
    email: null,
    firstname: null,
    lastname: null,
};

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setUser: (
            state,
            action: PayloadAction<Omit<UserState, 'isAuthed'>>
        ) => {
            state.isAuthed = true;
            state.login = action.payload.login;
            state.email = action.payload.email;
            state.firstname = action.payload.firstname;
            state.lastname = action.payload.lastname;
        },
        logout: (state) => {
            state.isAuthed = false;
            state.login = initialState.login;
            state.email = initialState.email;
            state.firstname = initialState.firstname;
            state.lastname = initialState.lastname;
        },
    },
});

export const userActions = userSlice.actions;

export default userSlice.reducer;
