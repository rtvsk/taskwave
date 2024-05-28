import { useDispatch, useSelector } from 'react-redux';
import { useEffect, useMemo } from 'react';
import Button from '@mui/material/Button';
import { Box, Typography } from '@mui/material';
// eslint-disable-next-line import/no-unresolved
import { useAutoAnimate } from '@formkit/auto-animate/react';

import { globalIsLoadingSelector } from '../slices/global/selectors';
import { Spinner } from '../components/spinner/Spinner';
import { isAuthedSelector } from '../slices/user/selectors';
import { taskGroupsSelector } from '../slices/taskGroup/selectors';
import { fetchTaskGroups } from '../actions/taskGroups/fetchTaskGroups';
import withContainerWrapper from '../hocs/withContainerWrapper';
import { AppDispatch } from '../store';
import { modalActions } from '../slices/modal/modalSlice';
import { addTaskGroupModalName } from '../constants/constants';

import { TaskGroup } from './TaskGroup';

const SimpleTaskGroups = () => {
    const dispatch = useDispatch<AppDispatch>();
    const isLoadingGlobal = useSelector(globalIsLoadingSelector);
    const isAuthed = useSelector(isAuthedSelector);
    const taskGroups = useSelector(taskGroupsSelector);
    const [parent] = useAutoAnimate();

    const handleClickOpenAdd = () => {
        dispatch(modalActions.set({ name: addTaskGroupModalName, data: null }));
    };

    useEffect(() => {
        if (isAuthed) {
            dispatch(fetchTaskGroups());
        }
    }, [isAuthed, dispatch]);

    const buttonAddTitle = useMemo(() => {
        if (!taskGroups.length) {
            return 'Add first one!';
        }

        return 'Add taskgroup';
    }, [taskGroups]);

    const isEmptyTaskGroups = Boolean(!taskGroups.length);

    const renderedTaskGroups = useMemo(() => {
        if (isEmptyTaskGroups) {
            return (
                <Box
                    display={'flex'}
                    alignItems={'center'}
                    justifyContent={'space-between'}
                >
                    <Typography variant='h5'>Taskgroups</Typography>
                    <Button variant='contained' onClick={handleClickOpenAdd}>
                        {buttonAddTitle}
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
                        {buttonAddTitle}
                    </Button>
                </Box>
                {taskGroups.map((taskGroup) => (
                    <TaskGroup key={taskGroup.id} {...taskGroup} />
                ))}
            </>
        );
    }, [taskGroups, buttonAddTitle, handleClickOpenAdd]);

    if (isLoadingGlobal) {
        return <Spinner />;
    }

    return <div ref={parent}>{renderedTaskGroups}</div>;
};

export const TaskGroups = withContainerWrapper(SimpleTaskGroups);
