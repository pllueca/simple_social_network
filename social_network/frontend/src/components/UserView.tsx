import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import type { User, Post } from '../types';
import { getUser, getUserPosts } from '../lib/api_client';
import { Link } from 'react-router-dom';

export function UserView() {
    const { userId } = useParams<{ userId: string }>();
    const [user, setUser] = useState<User | null>(null);
    const [posts, setPosts] = useState<Post[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!userId) return;

        Promise.all([
            getUser(userId),
            getUserPosts(userId)
        ]).then(([userData, postsData]) => {
            setUser(userData);
            setPosts(postsData);
        }).catch(() => {
            setError('Failed to load user data');
        });
    }, [userId]);

    if (error) return <div className="error">{error}</div>;
    if (!user) return <div>Loading...</div>;

    return (
        <div className="user-profile">
            <h1>{user.username}'s Profile</h1>
            <p>Member since: {new Date(user.created_at).toLocaleDateString()}</p>

            <h2>Posts</h2>
            <div className="user-posts">
                {posts.map(post => (
                    <div key={post.id} className="post-card">
                        <h3>
                            <Link to={`/posts/${post.id}`}>{post.title}</Link>
                        </h3>
                        <p>{post.body.substring(0, 100)}...</p>
                        <span className="date">{new Date(post.created_at).toLocaleDateString()}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
