import { RootState } from '../../store';

export const isAuthedSelector = (state: RootState) => state.user.isAuthed;
export const loginSelector = (state: RootState) => state.user.login;
