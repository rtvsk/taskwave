import { memo } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    TextField,
} from '@mui/material';

import { modalSelector } from '../../slices/modal/selectors';
import { AppDispatch } from '../../store';
import { addTaskGroupModalName } from '../../constants/constants';
import { addTaskGroup } from '../../actions/addTaskGroup';
import { modalActions } from '../../slices/modal/modalSlice';

export const AddTaskGroupModal = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    const modalData = useSelector(modalSelector);

    const isOpen = modalData.name === addTaskGroupModalName;
    const handleCloseModal = () => dispatch(modalActions.reset());

    return (
        <Dialog
            open={isOpen}
            onClose={handleCloseModal}
            PaperProps={{
                component: 'form',
                style: {
                    width: '100%',
                    maxWidth: '500px',
                },
                onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
                    event.preventDefault();
                    const formData = new FormData(event.currentTarget);
                    const formJson = Object.fromEntries(
                        (formData as any).entries()
                    );
                    const title = formJson['task-group-title'];
                    const description = formJson['task-group-description'];

                    dispatch(addTaskGroup({ title, description }));
                },
            }}
        >
            <DialogTitle>Adding a task group</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    Take your time! Stupid pigeon!
                </DialogContentText>
                <TextField
                    autoFocus
                    required
                    margin='dense'
                    id='task-group-title'
                    name='task-group-title'
                    label='Title'
                    type='task-group-title'
                    fullWidth
                    variant='standard'
                />
                <TextField
                    margin='dense'
                    id='task-group-description'
                    name='task-group-description'
                    label='Description'
                    type='task-group-description'
                    fullWidth
                    variant='standard'
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={handleCloseModal}>Cancel</Button>
                <Button type='submit'>Save</Button>
            </DialogActions>
        </Dialog>
    );
});
