import { useDispatch, useSelector } from 'react-redux';
import { useEffect, useMemo, Fragment } from 'react';
import Button from '@mui/material/Button';
import { Box, Typography, Divider, IconButton } from '@mui/material';
import EditNoteIcon from '@mui/icons-material/EditNote';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';

import { globalIsLoadingSelector } from '../slices/global/selectors';
import { Spinner } from '../components/spinner/Spinner';
import { isAuthedSelector } from '../slices/user/selectors';
import { taskGroupsSelector } from '../slices/taskGroup/selectors';
import { fetchTaskGroups } from '../actions/fetchTaskGroups';
import withContainerWrapper from '../hocs/withContainerWrapper';
import { deleteTaskGroup } from '../actions/deleteTaskGroup';
import { AppDispatch } from '../store';
import { modalActions } from '../slices/modal/modalSlice';
import {
    addTaskGroupModalName,
    editTaskGroupModalName,
} from '../constants/constants';

const SimpleTaskGroups = () => {
    const dispatch = useDispatch<AppDispatch>();
    const isLoadingGlobal = useSelector(globalIsLoadingSelector);
    const isAuthed = useSelector(isAuthedSelector);
    const taskGroups = useSelector(taskGroupsSelector);

    const handleClickOpenAdd = () => {
        dispatch(modalActions.set({ name: addTaskGroupModalName, data: null }));
    };

    useEffect(() => {
        if (isAuthed) {
            dispatch(fetchTaskGroups());
        }
    }, [isAuthed, dispatch]);

    const addButtonTitle = useMemo(() => {
        if (!taskGroups.length) {
            return 'Add first one!';
        }

        return 'Add +';
    }, [taskGroups]);

    const renderedTaskGroups = useMemo(() => {
        if (!taskGroups.length) {
            return (
                <Box
                    display={'flex'}
                    alignItems={'center'}
                    justifyContent={'space-between'}
                >
                    <Typography variant='h5'>Taskgroups</Typography>
                    <Button variant='contained' onClick={handleClickOpenAdd}>
                        {addButtonTitle}
                    </Button>
                </Box>
            );
        }

        return (
            <>
                <Box
                    display={'flex'}
                    alignItems={'center'}
                    justifyContent={'space-between'}
                    marginBottom={'50px'}
                >
                    <Typography variant='h5'>Taskgroups</Typography>
                    <Button variant='contained' onClick={handleClickOpenAdd}>
                        {addButtonTitle}
                    </Button>
                </Box>
                {taskGroups.map((taskGroup) => (
                    <Fragment key={taskGroup.id}>
                        {' '}
                        <Box
                            display={'flex'}
                            alignItems={'flex-start'}
                            justifyContent={'space-between'}
                        >
                            <Box>
                                <Typography
                                    variant='h6'
                                    color='text.primary'
                                    align='left'
                                >
                                    {taskGroup.title}
                                </Typography>
                                {taskGroup.description && (
                                    <Typography color='text.secondary'>
                                        {taskGroup.description}
                                    </Typography>
                                )}
                            </Box>
                            <Box display={'flex'} gap={'6px'}>
                                <IconButton
                                    size='small'
                                    onClick={() =>
                                        dispatch(
                                            modalActions.set({
                                                name: editTaskGroupModalName,
                                                data: taskGroup,
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
                                    onClick={() =>
                                        dispatch(deleteTaskGroup(taskGroup.id))
                                    }
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
                        <Divider
                            variant='fullWidth'
                            style={{ marginTop: '18px', marginBottom: '18px' }}
                        />
                    </Fragment>
                ))}
            </>
        );
    }, [taskGroups, addButtonTitle, dispatch]);

    if (isLoadingGlobal) {
        return <Spinner />;
    }

    return <div>{renderedTaskGroups}</div>;
};

export const TaskGroups = withContainerWrapper(SimpleTaskGroups);
