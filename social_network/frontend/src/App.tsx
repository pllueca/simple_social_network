import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import getUsers from './lib/api_client.tsx'

function App() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    const new_users = getUsers()
    console.log(new_users)
    new_users.then((res) => {
      console.log(res)
      setUsers(res)
    })
  }, [])

  return (
    <>
      <h1>Social Network</h1>
      <div className="card">
        users:
        {
          users.map(user => (
            <div>
              <h2>{user.username}</h2>
              <p>{user.id}, {user.created_at}</p>
            </div>
          ))
        }
      </div>

    </>
  )
}

export default App
