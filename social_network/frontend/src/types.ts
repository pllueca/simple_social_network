export interface User {
    id: string;
    username: string;
    created_at: string;
}

export interface Post {
    id: string;
    author_id: string;
    title: string;
    body: string;
    created_at: string;
}

export interface Comment {
    id: string;
    author_id: string;
    post_id: string;
    created_at: string;
    body: string;
}