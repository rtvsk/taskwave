import { RootState } from '../../store';

export const taskGroupIsLoadingSelector = (state: RootState) =>
    state.taskGroup.isLoading;

export const taskGroupsSelector = (state: RootState) =>
    state.taskGroup.taskGroups;
