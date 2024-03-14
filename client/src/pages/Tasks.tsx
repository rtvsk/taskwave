import { useSelector } from 'react-redux';

import { globalIsLoadingSelector } from '../slices/global/selectors';
import { Spinner } from '../components/spinner/Spinner';

export const Tasks = () => {
    const isLoadingGlobal = useSelector(globalIsLoadingSelector);

    if (isLoadingGlobal) {
        return <Spinner />;
    }

    return (
        <div>
            This is awesome task page! Enjoy it!8923472389472384723984723948
        </div>
    );
};
