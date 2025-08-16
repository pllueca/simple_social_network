import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Post, Comment } from '../types';
import { getPost, getPostComments } from '../lib/api_client';
import { PostComments } from './PostComments';

export function PostView() {
    const { postId } = useParams<{ postId: string }>();
    const [post, setPost] = useState<Post | null>(null);
    const [error, setError] = useState<string | null>(null);

    // load post and comments

    useEffect(() => {
        if (!postId) return;
        getPost(postId)
            .then(setPost)
            .catch(() => setError('Failed to load post'));
    }, [postId]);

    useEffect(() => {
        if (!postId) return;

    }, [postId]);

    if (error) return <div className="error">{error}</div>;
    if (!post) return <div>Loading...</div>;


    return (
        <div className="post-detail">
            <h1>{post.title}</h1>
            <div className="post-meta">
                <Link to={`/users/${post.author_id}`}>View Author</Link>
                <span className="date">{new Date(post.created_at).toLocaleDateString()}</span>
            </div>
            <div className="post-content">
                <p>{post.body}</p>
            </div>
            <PostComments />
        </div >
    );
}
