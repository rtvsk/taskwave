import { createSelector } from '@reduxjs/toolkit';

import { RootState } from '../../store';

export const tasksSelector = (state: RootState) => state.task.tasks;

export const tasksByTaskGroupIdSelector = (taskGroupId: string) =>
    createSelector(tasksSelector, (tasks) =>
        tasks.filter((task) => task.taskGroupId === taskGroupId)
    );
