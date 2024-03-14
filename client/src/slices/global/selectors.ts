import { RootState } from '../../store';

export const globalIsLoadingSelector = (state: RootState) =>
    state.global.isLoading;
