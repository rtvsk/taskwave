import { memo, useState } from 'react';
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
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';

import { modalSelector } from '../../slices/modal/selectors';
import { AppDispatch } from '../../store';
import { editTaskGroupModalName } from '../../constants/constants';
import { modalActions } from '../../slices/modal/modalSlice';
import { editTaskGroup } from '../../actions/taskGroups/editTaskGroup';

export const EditTaskGroupModal = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    const modalData = useSelector(modalSelector);

    const isOpen = modalData.name === editTaskGroupModalName;
    const handleCloseModal = () => dispatch(modalActions.reset());
    const id = modalData.data?.id || '';
    const [deadline, setDeadline] = useState(modalData.data?.deadline || null);

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

                    dispatch(
                        editTaskGroup({ id, title, description, deadline })
                    );
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
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker
                        format='DD.MM.YYYY'
                        defaultValue={
                            modalData.data?.deadline
                                ? dayjs(modalData.data?.deadline)
                                : null
                        }
                        onChange={(value) =>
                            setDeadline(value?.format('YYYY-MM-DD'))
                        }
                    />
                </LocalizationProvider>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleCloseModal}>Cancel</Button>
                <Button type='submit'>Save</Button>
            </DialogActions>
        </Dialog>
    );
});
