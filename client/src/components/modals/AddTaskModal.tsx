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
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

import { modalSelector } from '../../slices/modal/selectors';
import { AppDispatch } from '../../store';
import { addTaskModalName } from '../../constants/constants';
import { modalActions } from '../../slices/modal/modalSlice';
import { addTask } from '../../actions/task/addTask';

export const AddTaskModal = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    const modalData = useSelector(modalSelector);
    const [deadline, setDeadline] = useState(null);

    const isOpen = modalData.name === addTaskModalName;
    const handleCloseModal = () => dispatch(modalActions.reset());

    const taskGroupId = modalData.data?.taskGroupId;

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
                    const title = formJson['task-title'];
                    const description = formJson['task-description'];

                    dispatch(
                        addTask({ title, description, deadline, taskGroupId })
                    );
                },
            }}
        >
            <DialogTitle>Adding a task</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    Take your time! Stupid pigeon!
                </DialogContentText>
                <TextField
                    autoFocus
                    required
                    margin='dense'
                    id='task-title'
                    name='task-title'
                    label='Title'
                    type='task-title'
                    fullWidth
                    variant='standard'
                />
                <TextField
                    margin='dense'
                    id='task-description'
                    name='task-description'
                    label='Description'
                    type='task-description'
                    fullWidth
                    variant='standard'
                />
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker
                        format='DD.MM.YYYY'
                        onChange={(value) =>
                            // @ts-expect-error asdasd
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
