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
import { editTaskGroupModalName } from '../../constants/constants';
import { modalActions } from '../../slices/modal/modalSlice';
import { editTaskGroup } from '../../actions/editTaskGroup';

export const EditTaskGroupModal = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    const modalData = useSelector(modalSelector);

    const isOpen = modalData.name === editTaskGroupModalName;
    const handleCloseModal = () => dispatch(modalActions.reset());
    const id = modalData.data?.id || '';

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

                    dispatch(editTaskGroup({ id, title, description }));
                },
            }}
        >
            <DialogTitle>Editting a task group id</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    You can modify taskgroup's title and description right here
                </DialogContentText>
                <TextField
                    autoFocus
                    required
                    defaultValue={modalData.data?.title || ''}
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
                    defaultValue={modalData.data?.description || ''}
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
