export type SigninResponse = {
    access_token: string;
    token_type: string;
};

export type MeResponse = {
    // id: string;
    login: string;
    firstname: string | null;
    lastname: string | null;
    email: string;
};
