import { Fragment, useEffect, useState } from 'react';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import EditNoteIcon from '@mui/icons-material/EditNote';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import { Box, Typography, IconButton, Divider } from '@mui/material';
import { useDispatch } from 'react-redux';

import { ITaskGroup } from '../slices/taskGroup/taskGroupSlice';
import { deleteTaskGroup } from '../actions/taskGroups/deleteTaskGroup';
import { editTaskGroupModalName } from '../constants/constants';
import { convertDateYMDtoDMY } from '../helpers/helpers';
import { modalActions } from '../slices/modal/modalSlice';
import { AppDispatch } from '../store';
import { fetchTasksByTaskGroupId } from '../actions/task/fetchTasks';

import { Task } from './Task';

export const TaskGroup = (taskGroupProps: ITaskGroup) => {
    const { id: taskGroupId, title, description, deadline } = taskGroupProps;
    const dispatch = useDispatch() as AppDispatch;
    const [isOpen, setIsOpen] = useState(false);

    const toggleOpen = () => setIsOpen((prev) => !prev);

    useEffect(() => {
        taskGroupId && dispatch(fetchTasksByTaskGroupId(taskGroupId));
    }, [taskGroupId]);

    return (
        <Fragment key={taskGroupId}>
            {' '}
            <Box
                display={'flex'}
                alignItems={'flex-start'}
                justifyContent={'space-between'}
            >
                <Box
                    style={{ cursor: 'pointer', width: '100%' }}
                    onClick={toggleOpen}
                >
                    <Typography variant='h6' color='text.primary' align='left'>
                        {title}
                    </Typography>
                    {description && (
                        <Typography color='text.secondary'>
                            {description}
                        </Typography>
                    )}
                    {deadline && (
                        <Typography color='text.secondary'>
                            {`deadline: ${convertDateYMDtoDMY(deadline)}`}
                        </Typography>
                    )}
                </Box>
                <Box display={'flex'} gap={'6px'}>
                    <IconButton size='small' onClick={toggleOpen}>
                        {isOpen ? (
                            <ExpandLess
                                style={{
                                    width: '30px',
                                    height: '30px',
                                }}
                                color='primary'
                            />
                        ) : (
                            <ExpandMore
                                style={{
                                    width: '30px',
                                    height: '30px',
                                }}
                                color='primary'
                            />
                        )}
                    </IconButton>
                    <IconButton
                        size='small'
                        onClick={() =>
                            dispatch(
                                modalActions.set({
                                    name: editTaskGroupModalName,
                                    data: taskGroupProps,
                                })
                            )
                        }
                    >
                        <EditNoteIcon
                            style={{
                                width: '30px',
                                height: '30px',
                            }}
                            color='primary'
                        />
                    </IconButton>
                    <IconButton
                        size='small'
                        onClick={() => dispatch(deleteTaskGroup(taskGroupId))}
                    >
                        <DeleteForeverIcon
                            style={{
                                width: '30px',
                                height: '30px',
                            }}
                            color='error'
                        />
                    </IconButton>
                </Box>
            </Box>
            {isOpen && <Task taskGroupId={taskGroupId} />}
            <Divider
                variant='fullWidth'
                style={{ marginTop: '18px', marginBottom: '18px' }}
            />
        </Fragment>
    );
};
