import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AuthHeader } from '../components/auth/AuthHeader';
import { AuthHero } from '../components/auth/AuthHero';
import { SignInForm } from '../components/auth/SignInForm';
import { SignUpForm } from '../components/auth/SignUpForm';

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();

  const [mode, setMode] = useState(
    location.pathname.includes('signup') || location.pathname.includes('register') ? 'signup' : 'signin'
  );

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);

  const [fullName, setFullName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const clearMessages = () => {
    setErrorMessage('');
    setSuccessMessage('');
  };

  const handleSignIn = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    clearMessages();

    const cleanInput = (email || '').trim();
    if (!cleanInput) {
      setErrorMessage('Please enter your official email or username.');
      return;
    }
    if (!password) {
      setErrorMessage('Please enter your password.');
      return;
    }

    try {
      setLoading(true);
      const res = await login(cleanInput, password);
      if (res && res.success) {
        setSuccessMessage(`Access Granted. Welcome, ${res.user?.name || 'Officer'}.`);
        const targetPath = res.user?.role === 'admin' ? '/' : '/explorer';
        setTimeout(() => navigate(targetPath), 300);
      } else {
        setErrorMessage(res?.error || 'Authentication failed. Please verify credentials.');
      }
    } catch (err) {
      setErrorMessage(err?.message || 'Authentication error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    clearMessages();

    if (!fullName.trim() || !regEmail.trim() || !regPassword) {
      setErrorMessage('Please fill in your name, email, and password.');
      return;
    }

    try {
      setLoading(true);
      const res = await register({
        fullName: fullName.trim(),
        email: regEmail.trim(),
        password: regPassword,
        ministry: 'Ministry of Statistics and Programme Implementation',
        designation: 'Operations Employee',
        role: 'employee'
      });
      if (res && res.success) {
        setSuccessMessage('Officer identity registered successfully. Redirecting...');
        const targetPath = res.user?.role === 'admin' ? '/' : '/explorer';
        setTimeout(() => navigate(targetPath), 400);
      } else {
        setErrorMessage(res?.error || 'Failed to register officer credentials.');
      }
    } catch (err) {
      setErrorMessage(err?.message || 'Registration error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    document.documentElement.classList.add('auth-page');
    document.body.classList.add('auth-page');
    return () => {
      document.documentElement.classList.remove('auth-page');
      document.body.classList.remove('auth-page');
    };
  }, []);

  return (
    <div className="auth-viewport-root h-[100dvh] max-h-[100dvh] overflow-hidden bg-white text-slate-900 flex flex-col justify-between font-sans">
      <AuthHeader />

      <main className="flex-1 flex flex-col items-center justify-center px-4 md:px-8 py-2 overflow-y-auto lg:overflow-hidden">
        <div className="grid items-center gap-8 lg:gap-12 max-w-lg lg:grid-cols-2 lg:max-w-5xl w-full my-auto">
          <AuthHero
            mode={mode}
            setMode={setMode}
            onClearMessages={clearMessages}
          />

          <div className="max-w-md lg:ml-auto w-full">
            {mode === 'signin' ? (
              <SignInForm
                email={email}
                setEmail={setEmail}
                password={password}
                setPassword={setPassword}
                rememberMe={rememberMe}
                setRememberMe={setRememberMe}
                handleSignIn={handleSignIn}
                loading={loading}
                errorMessage={errorMessage}
                successMessage={successMessage}
              />
            ) : (
              <SignUpForm
                fullName={fullName}
                setFullName={setFullName}
                regEmail={regEmail}
                setRegEmail={setRegEmail}
                regPassword={regPassword}
                setRegPassword={setRegPassword}
                handleSignUp={handleSignUp}
                loading={loading}
                errorMessage={errorMessage}
                successMessage={successMessage}
              />
            )}
          </div>
        </div>
      </main>

      <footer className="w-full bg-white border-t border-slate-100 py-2.5 text-center text-[11px] text-slate-500 shrink-0">
        Ministry of Statistics and Programme Implementation (MoSPI) • Government of India
      </footer>
    </div>
  );
};

export default LoginPage;
