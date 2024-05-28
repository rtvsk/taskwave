import { useDispatch, useSelector } from 'react-redux';
import { Box, Button, IconButton, Typography } from '@mui/material';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import EditNoteIcon from '@mui/icons-material/EditNote';
import { Fragment } from 'react/jsx-runtime';
import { useCallback } from 'react';

import { tasksByTaskGroupIdSelector } from '../slices/task/selectors';
import { AppDispatch, RootState } from '../store';
import { modalActions } from '../slices/modal/modalSlice';
import { addTaskModalName, editTaskModalName } from '../constants/constants';
import { deleteTask } from '../actions/task/deleteTask';
import { convertDateYMDtoDMY } from '../helpers/helpers';
import { ITask } from '../slices/task/taskSlice';

interface TaskProps {
    taskGroupId: string;
}

export const Task = (props: TaskProps) => {
    const { taskGroupId } = props;
    const dispatch = useDispatch() as AppDispatch;
    const selectTasksByGroupId = tasksByTaskGroupIdSelector(taskGroupId);
    const tasks = useSelector((state: RootState) =>
        selectTasksByGroupId(state)
    );

    const hasNoTasks = Boolean(!tasks.length);

    const openModalAddTask = () => {
        dispatch(
            modalActions.set({ name: addTaskModalName, data: { taskGroupId } })
        );
    };

    const iconStyle = {
        width: '22px',
        height: '22px',
    };

    const onOpenEditTaskModal = useCallback((task: ITask) => {
        dispatch(
            modalActions.set({
                name: editTaskModalName,
                data: task,
            })
        );
    }, []);

    const renderedTasks = tasks.map((task) => (
        <Box
            key={task.id}
            display='flex'
            alignItems='flex-start'
            justifyContent='flex-start'
            style={{ margin: '20px 0px 20px 15px' }}
            gap={'6px'}
        >
            <IconButton
                size='small'
                onClick={() => {
                    dispatch(
                        deleteTask({
                            taskGroupId: task.taskGroupId,
                            taskId: task.id,
                        })
                    );
                }}
            >
                <DeleteForeverIcon style={iconStyle} color='error' />
            </IconButton>
            <IconButton size='small' onClick={() => onOpenEditTaskModal(task)}>
                <EditNoteIcon style={iconStyle} color='primary' />
            </IconButton>
            <Box display={'flex'} flexDirection={'column'}>
                <Typography variant='h6'>{task.title}</Typography>
                <Typography variant='body1'>{task.description}</Typography>
                {task.deadline && (
                    <Typography color='text.secondary' variant='body2'>
                        {`untill: ${convertDateYMDtoDMY(task.deadline)}`}
                    </Typography>
                )}
            </Box>
        </Box>
    ));

    return (
        <Fragment>
            <Box
                display='flex'
                alignItems='center'
                justifyContent='space-between'
                style={{ margin: '20px 0px 20px 15px' }}
            >
                <Typography variant='subtitle1'>
                    {hasNoTasks ? 'You havent any tasks yet' : 'Your tasks:'}
                </Typography>
                <Button
                    style={{ padding: '4px 8px' }}
                    variant='outlined'
                    onClick={openModalAddTask}
                >
                    {'Add task'}
                </Button>
            </Box>
            {renderedTasks}
        </Fragment>
    );
};
