import { TOKEN_PREFIX } from '../constants/constants';

export class Token {
    static get(): string | null {
        return localStorage.getItem(TOKEN_PREFIX);
    }

    static set(token: string): void {
        localStorage.setItem(TOKEN_PREFIX, token);
    }

    static delete(): void {
        localStorage.removeItem(TOKEN_PREFIX);
    }
}

export const getGreetingByTime = (): string => {
    const currentTime = new Date().getHours();

    if (currentTime >= 0 && currentTime < 6) {
        return 'Good night!';
    } else if (currentTime >= 6 && currentTime < 12) {
        return 'Good morning!';
    } else if (currentTime >= 12 && currentTime < 18) {
        return 'Good afternoon!';
    } else {
        return 'Good evening!';
    }
};
