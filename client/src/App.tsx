import * as React from 'react';
import { Switch, Route, withRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { useSelector } from 'react-redux';

import { SignIn } from './pages/SignIn';
import { Page404 } from './pages/Page404';
import { SignUp } from './pages/SignUp';
import { Tasks } from './pages/Tasks';
import { Header } from './components/header/Header';
import { Spinner } from './components/spinner/Spinner';
import { globalIsLoadingSelector } from './slices/global/selectors';
import { useInitial } from './hooks/useInitial';

export const App = withRouter(() => {
    const isLoading = useSelector(globalIsLoadingSelector);

    useInitial();

    if (isLoading) {
        return <Spinner />;
    }

    return (
        <React.Fragment>
            <Header />
            <Switch>
                <Route path='/sign-in'>
                    <SignIn />
                </Route>
                <Route path='/sign-up'>
                    <SignUp />
                </Route>
                <Route path='/tasks'>
                    <Tasks />
                </Route>
                <Route path='*'>
                    <Page404 />
                </Route>
            </Switch>
            <ToastContainer />
        </React.Fragment>
    );
});
