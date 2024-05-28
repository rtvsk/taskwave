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
import { editTaskModalName } from '../../constants/constants';
import { modalActions } from '../../slices/modal/modalSlice';
import { ITask } from '../../slices/task/taskSlice';
import { editTask } from '../../actions/task/editTask';

export const EditTaskModal = memo(() => {
    const dispatch = useDispatch<AppDispatch>();
    const modalData = useSelector(modalSelector);
    const [deadline, setDeadline] = useState(modalData.data?.deadline || null);

    const isOpen = modalData.name === editTaskModalName;
    const handleCloseModal = () => dispatch(modalActions.reset());

    if (!isOpen) {
        return null;
    }

    const { taskGroupId, id, is_done } = modalData.data as ITask;

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
                        editTask({
                            taskGroupId,
                            id,
                            title,
                            description,
                            deadline,
                            is_done,
                        })
                    );
                },
            }}
        >
            <DialogTitle>Editting a task</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    You can modify task's title and description right here
                </DialogContentText>
                <TextField
                    autoFocus
                    required
                    defaultValue={modalData.data?.title || ''}
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
                    defaultValue={modalData.data?.description || ''}
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
