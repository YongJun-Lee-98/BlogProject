import React, { useState } from 'react';
import LoginModal from './LoginModal';

const App = () => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  const handleOpenModal = () => setIsLoginModalOpen(true);
  const handleCloseModal = () => setIsLoginModalOpen(false);
  const handleLoginSuccess = () => {
    alert('로그인 성공');
    // 로그인 성공 후 처리 (예: 사용자 정보 저장, 페이지 리다이렉트 등)
  };

  return (
    <div>
      <button onClick={handleOpenModal}>로그인</button>

      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={handleCloseModal}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
};

export default App;
