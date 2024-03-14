import { RootState } from '../../store';

export const taskGroupIsLoadingSelector = (state: RootState) =>
    state.taskGroup.isLoading;
