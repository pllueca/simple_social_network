import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import type { Comment } from '../types';
import { getPostComments } from '../lib/api_client';

export function PostComments() {
    const { postId } = useParams<{ postId: string }>();
    const [comments, setComments] = useState<Comment[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!postId) return;

        getPostComments(postId)
            .then(setComments)
            .catch(() => setError('Failed to load post comments'));
    }, [postId]);


    if (error) return <div className="error">{error}</div>;
    if (comments === null) return <div>Loading Comments...</div>;
    if (comments.length === 0) return <div> No comments.</div>;

    return <div>
        Comments:
        {comments.map((comment) => <div key={`comment-${comment.id}`}>
            {comment.body}
            by
            <Link to={`/users/${comment.author_id}`}>
                {comment.author_id}
            </Link>
            at
            <span className="date">
                {new Date(comment.created_at).toLocaleDateString()}
            </span>
        </div>
        )}
    </div>;
}