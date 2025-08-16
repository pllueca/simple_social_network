import { useEffect, useState } from 'react';
import type { Post } from '../types';
import { listPosts } from '../lib/api_client';
import { Link } from 'react-router-dom';

export function HomePage() {
    const [posts, setPosts] = useState<Post[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        listPosts()
            .then(posts => {
                // Sort posts by creation date, most recent first
                const sortedPosts = [...posts].sort(
                    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
                );
                setPosts(sortedPosts);
            })
            .catch(err => setError('Failed to load posts'));
    }, []);

    if (error) return <div className="error">{error}</div>;

    return (
        <div className="posts-list">
            <h1>Recent Posts</h1>
            {posts.map(post => (
                <div key={post.id} className="post-card">
                    <h2>
                        <Link to={`/posts/${post.id}`}>{post.title}</Link>
                    </h2>
                    <p>{post.body.substring(0, 100)}...</p>
                    <div className="post-meta">
                        <Link to={`/users/${post.author_id}`}>View Author</Link>
                        <span className="date">{new Date(post.created_at).toLocaleDateString()}</span>
                    </div>
                </div>
            ))}
        </div>
    );
}
