import { configureStore, combineReducers } from '@reduxjs/toolkit';

import userReducer from './slices/user/userSlice';
import globalReducer from './slices/global/globalSlice';
import taskGroupReducer from './slices/taskGroup/taskGroupSlice';
import modalReducer from './slices/modal/modalSlice';

const rootReducer = combineReducers({
    user: userReducer,
    global: globalReducer,
    taskGroup: taskGroupReducer,
    modal: modalReducer,
});

export const store = configureStore({
    reducer: rootReducer,
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
