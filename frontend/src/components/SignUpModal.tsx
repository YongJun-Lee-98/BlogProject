import React, { useState } from 'react';
import axios from 'axios';
import Modal from 'react-modal';

// Modal의 루트 요소 설정
Modal.setAppElement('#root');

interface SignUpModalProps {
    isOpen: boolean;
    onRequestClose: () => void;
}

const SignUpModal: React.FC<SignUpModalProps> = ({ isOpen, onRequestClose }) => {
    const [userId, setUserId] = useState<string>('');
    const [blogName, setBlogName] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [confirmPassword, setConfirmPassword] = useState<string>('');
    const [errorMessage, setErrorMessage] = useState<string>('');

    // API_BASE_URL 상수 추가
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // 비밀번호 확인
        if (password !== confirmPassword) {
            setErrorMessage('Password do not match!');
            return;
        }

        try {
            // URL 경로 수정
            const response = await axios.post(`${API_BASE_URL}/api/accounts/signup/`, {
                user_id: userId,
                blog_name: blogName,
                password,
                password_confirm: confirmPassword,
            });

            if (response.status === 201) {
                // 성공적으로 회원가입된 경우
                setErrorMessage('');
                onRequestClose(); // 모달 닫기
                alert('Account created successfully!');
            }
        } catch (error) {
            // 에러 메시지 설정
            setErrorMessage('Error during signup!');
        }
    };
    return (
        <Modal isOpen={isOpen} onRequestClose={onRequestClose} contentLabel='Sign Up Modal'>
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="userId">User ID:</label>
                    <input
                      type="text"
                      id="userId"
                      value={userId}
                      onChange={(e) => setUserId(e.target.value)}
                      required
                    />
                </div>
                <div>
                    <label htmlFor="blogName">blogName:</label>
                    <input
                      type="text"
                      id="blogName"
                      value={blogName}
                      onChange={(e) => setBlogName(e.target.value)}
                      required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                      type="password"
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                </div>
                <div>
                    <label htmlFor="passwordConfirm">Confirm Password:</label>
                    <input
                      type="password"
                      id="passwordConfirm"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                </div>

                {errorMessage && <p style={{ color: 'red' }}> {errorMessage}</p>}

                <button type="submit">Sign Up</button>
            </form>
        </Modal>
    );
};

export default SignUpModal;