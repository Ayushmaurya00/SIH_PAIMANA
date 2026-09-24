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
      <h1 className="text-slate-900 text-3xl font-bold mb-8">
        Sign in
      </h1>

      {errorMessage && (
        <div className="mb-6 p-3 rounded-md bg-red-50 border border-red-200 text-red-700 text-sm font-medium">
          {errorMessage}
        </div>
      )}

      {successMessage && (
        <div className="mb-6 p-3 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm font-medium">
          {successMessage}
        </div>
      )}

      {infoMessage && (
        <div className="mb-6 p-3 rounded-md bg-blue-50 border border-blue-200 text-blue-700 text-sm font-medium">
          {infoMessage}
        </div>
      )}

      <form onSubmit={handleSignIn} className="space-y-6">
        <div>
          <label htmlFor="email" className="mb-2 text-slate-900 font-medium text-sm inline-block">
            Official Email / Username
          </label>
          <input
            type="text"
            id="email"
            name="email"
            autoComplete="username"
            value={email}
            onChange={(e) => { setEmail(e.target.value); setInfoMessage(''); }}
            placeholder="admin@mospi.gov.in or Username"
            required
            className="px-3 py-2.5 text-sm text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div>
          <label htmlFor="password" className="mb-2 text-slate-900 font-medium text-sm inline-block">
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
            className="px-3 py-2.5 text-sm text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div className="flex items-center justify-between flex-wrap gap-2">
          <label className="flex items-center cursor-pointer select-none">
            <input
              id="remember"
              name="remember"
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-600 cursor-pointer"
            />
            <span className="ml-2.5 text-sm text-slate-700">
              Remember me
            </span>
          </label>

          <button
            type="button"
            onClick={handleForgotPassword}
            className="text-sm font-medium text-blue-700 hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded bg-transparent p-0 border-none cursor-pointer"
          >
            Forgot password?
          </button>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 px-3.5 text-sm rounded-md font-semibold cursor-pointer text-white border border-blue-600 bg-blue-600 hover:bg-blue-700 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </form>

      <div className="mt-8 pt-6 border-t border-slate-100 text-xs text-slate-500">
        <p className="font-semibold text-slate-700 mb-1.5">Official Credentials Reference:</p>
        <div className="space-y-1 text-[11px] text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
          <div><span className="font-medium text-slate-900">Admin:</span> admin@mospi.gov.in / Admin@MoSPI2026!</div>
          <div><span className="font-medium text-slate-900">Officer:</span> rajesh.sharma@mospi.gov.in / Paimana@123</div>
        </div>
      </div>
    </div>
  );
};

export default SignInForm;
