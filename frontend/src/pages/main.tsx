import React, { useState } from 'react'
import Button from '../components/Button'
import LoginModal from '../components/LoginModal'
import SignUpModal from '../components/SignUpModal'
// import './main.css'

/* main 페이지 구성 /GET이 유저 정보까지 넘어오면 유저의 페이지로 바뀜
유저 정보 없이 main으로 가면 전체 유저중 최신 글 노출
블로그 대문 / 로그인 페이지로 이동 / 새글 쓰기
post 내용 보이기
---
카테고리
---
ads-banner - container로 구성(맨 하단에서 dom 위의 dom 이름 이후에 찾아서 적어두기)
*/


const HomePage: React.FC = () => {

    const handleClick = () => {
        alert(' Button clicked! ');
    };
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
    const openLoginModal = () => setIsLoginModalOpen(true);
    const closeLoginModal = () => setIsLoginModalOpen(false);

    const [isSignUpModalOpen, setIsSignUpModalOpen] = useState(false);
    const openSignUpModal = () => setIsSignUpModalOpen(true);
    const closeSignUpModal = () => setIsSignUpModalOpen(false);

    return (
        <div>
            <Button label="로그인" onClick={openLoginModal} />
            <LoginModal isOpen={isLoginModalOpen} onClose={closeLoginModal} />
            <Button label="Click Me" onClick={handleClick} />
            <Button label="회원가입" onClick={openSignUpModal} />
            <SignUpModal isOpen={isSignUpModalOpen} onRequestClose={closeSignUpModal} />
            <h2>Python Blog</h2>
            
        </div>
    );
};

export default HomePage;