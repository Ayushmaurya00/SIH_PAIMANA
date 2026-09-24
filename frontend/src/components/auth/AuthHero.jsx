import React from 'react';

export const AuthHero = ({ mode, setMode, onClearMessages }) => {
  const isSignIn = mode === 'signin';

  const handleToggle = (newMode) => {
    setMode(newMode);
    if (onClearMessages) onClearMessages();
  };

  return (
    <div>
      <h2 className="text-4xl font-bold text-slate-900 !leading-tight lg:text-5xl">
        {isSignIn
          ? 'Central Infrastructure Monitoring & Decision Support'
          : 'Register Monitoring Officer Credentials'}
      </h2>
      <p className="text-base mt-6 text-slate-600 leading-relaxed">
        {isSignIn
          ? 'Access real-time MoSPI Flash Report telemetry, physical vs. financial S-curves, and machine learning early-warning risk analytics across ₹35.38 Lakh Crore in Central Sector infrastructure projects.'
          : 'Create verified administrative credentials to review project dossiers, milestone slippages, and prescriptive delay mitigation playbooks.'}
      </p>

      <div className="text-sm mt-6 text-slate-900 lg:mt-12">
        {isSignIn ? (
          <>
            Don't have an account{' '}
            <button
              type="button"
              onClick={() => handleToggle('signup')}
              className="text-blue-700 font-medium hover:underline ml-1 cursor-pointer bg-transparent border-none p-0 inline"
            >
              Register here
            </button>
          </>
        ) : (
          <>
            Already have an account?{' '}
            <button
              type="button"
              onClick={() => handleToggle('signin')}
              className="text-blue-700 font-medium hover:underline ml-1 cursor-pointer bg-transparent border-none p-0 inline"
            >
              Sign in here
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default AuthHero;
