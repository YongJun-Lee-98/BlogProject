// src/components/LoginModal.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import './LoginModal.css';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoginSuccess?: () => void;
}

interface TokenResponse {
  access: string;
  refresh: string;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post<TokenResponse>(
        `${API_BASE_URL}/api/accounts/token/`,
        { 
          user_id: username,
          password: password 
        }
      );

      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      setUsername('');
      setPassword('');
      setErrorMessage('');
      
      if (onLoginSuccess) {
        onLoginSuccess();
      }
      
      onClose();
      
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 100);
      
    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        setErrorMessage(
          error.response?.data?.detail || 
          error.response?.data?.message || 
          '로그인에 실패했습니다.'
        );
      } else {
        setErrorMessage('알 수 없는 오류가 발생했습니다.');
      }
    }
  };

  useEffect(() => {
    if (!isOpen) {
      setUsername('');
      setPassword('');
      setErrorMessage('');
    }
  }, [isOpen]);

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Login Modal"
      className="modal-content"
      overlayClassName='modal-overlay'
    >
      <h2>Login</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <button onClick={onClose}>Close</button>
    </Modal>
  );
};

export default LoginModal;
