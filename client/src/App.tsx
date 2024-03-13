import * as React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';

import { SignIn } from './pages/SignIn';
import { Page404 } from './pages/Page404';
import { SignUp } from './pages/SignUp';
import { Tasks } from './pages/Tasks';

export const App = () => {
    return (
        <React.Fragment>
            <Router>
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
            </Router>
            <ToastContainer />
        </React.Fragment>
    );
};
