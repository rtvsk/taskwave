import { RootState } from '../store';

export const isAuthedSelector = (state: RootState) => state.user.isAuthed;
