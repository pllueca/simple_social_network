import { useEffect, useState } from 'react';
import type { User } from '../types';
import { listUsers } from '../lib/api_client';
import { Link } from 'react-router-dom';

export function UsersListView() {
    const [users, setUsers] = useState<User[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        listUsers()
            .then(setUsers)
            .catch(() => setError('Failed to load users'));
    }, []);

    if (error) return <div className="error">{error}</div>;

    return (
        <div className="users-list">
            <h1>Users</h1>
            {users.map(user => (
                <div key={user.id} className="user-card">
                    <h2>
                        <Link to={`/users/${user.id}`}>{user.username}</Link>
                    </h2>
                    <p>Joined: {new Date(user.created_at).toLocaleDateString()}</p>
                </div>
            ))}
        </div>
    );
}
