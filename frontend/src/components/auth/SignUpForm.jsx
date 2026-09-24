import React from 'react';

export const SignUpForm = ({
  fullName,
  setFullName,
  regEmail,
  setRegEmail,
  regPassword,
  setRegPassword,
  handleSignUp,
  loading,
  errorMessage,
  successMessage,
}) => {
  return (
    <div className="w-full">
      <h1 className="text-slate-900 text-3xl font-bold mb-8">
        Create Account
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

      <form onSubmit={handleSignUp} className="space-y-6">
        <div>
          <label htmlFor="reg-name" className="mb-2 text-slate-900 font-medium text-sm inline-block">
            Full Name & Rank
          </label>
          <input
            type="text"
            id="reg-name"
            name="name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="e.g. Dr. Rajesh Sharma, IAS"
            required
            className="px-3 py-2.5 text-sm text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div>
          <label htmlFor="reg-email" className="mb-2 text-slate-900 font-medium text-sm inline-block">
            Official Email / Username
          </label>
          <input
            type="text"
            id="reg-email"
            name="email"
            autoComplete="username"
            value={regEmail}
            onChange={(e) => setRegEmail(e.target.value)}
            placeholder="officer@mospi.gov.in"
            required
            className="px-3 py-2.5 text-sm text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <div>
          <label htmlFor="reg-password" className="mb-2 text-slate-900 font-medium text-sm inline-block">
            Password
          </label>
          <input
            type="password"
            id="reg-password"
            name="password"
            value={regPassword}
            onChange={(e) => setRegPassword(e.target.value)}
            placeholder="••••••••"
            required
            className="px-3 py-2.5 text-sm text-slate-900 rounded-md bg-white w-full border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600 transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 px-3.5 text-sm rounded-md font-semibold cursor-pointer text-white border border-blue-600 bg-blue-600 hover:bg-blue-700 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Creating account...' : 'Create Account'}
        </button>
      </form>
    </div>
  );
};

export default SignUpForm;
