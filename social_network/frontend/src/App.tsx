import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HomePage } from './components/HomePage';
import { UsersListView } from './components/UsersListView';
import { UserView } from './components/UserView';
import { PostView } from './components/PostView';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/users">Users</Link></li>
          </ul>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/users" element={<UsersListView />} />
            <Route path="/users/:userId" element={<UserView />} />
            <Route path="/posts/:postId" element={<PostView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
