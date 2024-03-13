import { useSelector } from 'react-redux';
import { useHistory } from 'react-router-dom';

import { isAuthedSelector } from '../slices/selectors';

export const Tasks = () => {
    const isAuthed = useSelector(isAuthedSelector);
    const history = useHistory();

    if (!isAuthed) {
        // eslint-disable-next-line no-console
        console.log('<Tasks/> not authed, redirect to sign-in');

        history.push('/sign-in');

        return;
    }

    return (
        <div>
            This is awesome task page! Enjoy it!8923472389472384723984723948
        </div>
    );
};
