import React, { useState, useEffect } from 'react';
import { authAPI } from '../api';
import { User } from '../types';

interface LoginProps {
  onLogin: (user: User, token: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [isSignup, setIsSignup] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'child'
  });
  const [availableChildren, setAvailableChildren] = useState<any[]>([]);
  const [selectedChildren, setSelectedChildren] = useState<number[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isSignup && formData.role === 'parent') {
      loadAvailableChildren();
    }
  }, [isSignup, formData.role]);

  const loadAvailableChildren = async () => {
    try {
      const response = await authAPI.getAvailableChildren();
      setAvailableChildren(response.data);
    } catch (error) {
      console.error('Error loading children:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isSignup) {
        await authAPI.signup(formData.username, formData.email, formData.password, formData.role, undefined, selectedChildren);
        alert('Account created successfully! Please login.');
        setIsSignup(false);
        setSelectedChildren([]);
      } else {
        const response = await authAPI.login(formData.username, formData.password);
        onLogin(response.data.user, response.data.access_token);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h1>NoteNext</h1>
        <h2>{isSignup ? 'Sign Up' : 'Login'}</h2>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            required
          />
          
          {isSignup && (
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          )}
          
          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            required
          />
          
          {isSignup && (
            <select
              value={formData.role}
              onChange={(e) => {
                setFormData({ ...formData, role: e.target.value });
                setSelectedChildren([]);
              }}
            >
              <option value="child">Child</option>
              <option value="parent">Parent</option>
            </select>
          )}
          
          {isSignup && formData.role === 'parent' && availableChildren.length > 0 && (
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Select Children:</label>
              {availableChildren.map(child => (
                <label key={child.id} style={{ display: 'block', marginBottom: '0.3rem' }}>
                  <input
                    type="checkbox"
                    checked={selectedChildren.includes(child.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedChildren([...selectedChildren, child.id]);
                      } else {
                        setSelectedChildren(selectedChildren.filter(id => id !== child.id));
                      }
                    }}
                    style={{ marginRight: '0.5rem' }}
                  />
                  {child.username}
                </label>
              ))}
            </div>
          )}
          
          {error && <div className="error">{error}</div>}
          
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : (isSignup ? 'Sign Up' : 'Login')}
          </button>
        </form>
        
        <p>
          {isSignup ? 'Already have an account?' : "Don't have an account?"}
          <button
            type="button"
            className="link-button"
            onClick={() => setIsSignup(!isSignup)}
          >
            {isSignup ? 'Login' : 'Sign Up'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default Login;