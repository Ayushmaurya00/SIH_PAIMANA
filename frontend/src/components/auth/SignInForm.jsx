import React, { useState } from 'react';

export const SignInForm = ({
  email,
  setEmail,
  password,
  setPassword,
  rememberMe,
  setRememberMe,
  handleSignIn,
  loading,
  errorMessage,
  successMessage,
}) => {
  const [infoMessage, setInfoMessage] = useState('');

  const handleForgotPassword = () => {
    if (!email.trim()) {
      setInfoMessage('Enter your official email or username above, then click Forgot password.');
      return;
    }
    setInfoMessage(`Password reset link dispatched to ${email.trim()}. Please verify your mailbox.`);
  };

  return (
    <div className="w-full">
      <h1 className="text-slate-900 text-2xl font-bold mb-4">
        Sign in
      </h1>

      {errorMessage && (
        <div className="mb-3 p-2 rounded-md bg-red-50 border border-red-200 text-red-700 text-xs font-medium">
          {errorMessage}
        </div>
      )}

      {successMessage && (
        <div className="mb-3 p-2 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-medium">
          {successMessage}
        </div>
      )}

      {infoMessage && (
        <div className="mb-3 p-2 rounded-md bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium">
          {infoMessage}
        </div>
      )}

      <form onSubmit={handleSignIn} className="space-y-3.5">
        <div>
          <label htmlFor="email" className="mb-1 text-slate-800 font-semibold text-xs inline-block">
            Official Email / Username
          </label>
          <input
            type="text"
            id="email"
            name="email"
            autoComplete="username"
            value={email}
            onChange={(e) => { setEmail(e.target.value); setInfoMessage(''); }}
            placeholder="admin@mospi.gov.in or employee_id"
            required
            className="px-3 py-2 text-xs text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div>
          <label htmlFor="password" className="mb-1 text-slate-800 font-semibold text-xs inline-block">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => { setPassword(e.target.value); setInfoMessage(''); }}
            placeholder="••••••••"
            required
            className="px-3 py-2 text-xs text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div className="flex items-center justify-between flex-wrap gap-2 pt-0.5">
          <label className="flex items-center cursor-pointer select-none">
            <input
              id="remember"
              name="remember"
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="h-3.5 w-3.5 rounded border-slate-300 text-blue-600 focus:ring-blue-600 cursor-pointer"
            />
            <span className="ml-2 text-xs text-slate-600">
              Remember me
            </span>
          </label>

          <button
            type="button"
            onClick={handleForgotPassword}
            className="text-xs font-medium text-blue-700 hover:underline focus:outline-none rounded bg-transparent p-0 border-none cursor-pointer"
          >
            Forgot password?
          </button>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-3 text-xs rounded-md font-bold cursor-pointer text-white border border-blue-600 bg-blue-600 hover:bg-blue-700 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50 mt-1"
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
    </div>
  );
};

export default SignInForm;
