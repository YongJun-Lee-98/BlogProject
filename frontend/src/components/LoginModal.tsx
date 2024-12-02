// src/components/LoginModal.tsx
import React, { useState } from 'react';
import axios from 'axios';
import Modal from 'react-modal';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/accounts/token/', {
        username,
        password,
      });

      // 로그인 성공 시, JWT 토큰 저장
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      onClose(); // 모달 닫기
      window.location.href = '/dashboard'; // 대시보드로 리다이렉트

    } catch (error) {
      alert('Invalid username or password');
    }
  };

  return (
    <Modal isOpen={isOpen} onRequestClose={onClose} contentLabel="Login Modal">
      <h2>Login</h2>
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
