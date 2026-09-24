import React, { createContext, useContext, useState, useEffect } from 'react';
import { DEMO_PROFILES, V3_DEMO_EMAIL, V3_DEMO_PROFILE } from './demoProfiles';
import { loginOfficer, registerOfficer } from '../api/client';

export { DEMO_PROFILES, V3_DEMO_EMAIL, V3_DEMO_PROFILE };

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('paimana_auth_user');
      if (stored) return JSON.parse(stored);
    } catch (e) {
      console.error('Failed to parse stored auth session:', e);
    }
    return null;
  });

  const [token, setToken] = useState(() => localStorage.getItem('paimana_auth_token') || null);

  useEffect(() => {
    if (user) {
      localStorage.setItem('paimana_auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('paimana_auth_user');
    }
  }, [user]);

  useEffect(() => {
    if (token) {
      localStorage.setItem('paimana_auth_token', token);
    } else {
      localStorage.removeItem('paimana_auth_token');
    }
  }, [token]);

  const login = async (email, password) => {
    const rawInput = (email || '').trim();
    if (!rawInput) {
      return { success: false, error: 'Please enter your official email or username.' };
    }
    if (!password) {
      return { success: false, error: 'Please enter your password.' };
    }

    try {
      const data = await loginOfficer(rawInput, password);
      if (data && data.token) {
        setUser(data);
        setToken(data.token);
        return { success: true, user: data };
      }
      return { success: false, error: 'Authentication failed. Please verify credentials.' };
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Authentication failed. Please verify credentials.';
      return { success: false, error: msg };
    }
  };

  const register = async (userData) => {
    const rawEmail = (userData.email || '').trim();
    if (!rawEmail || !userData.password) {
      return { success: false, error: 'Please provide email and password.' };
    }

    try {
      const data = await registerOfficer({
        full_name: userData.fullName || 'Official Officer',
        email: rawEmail,
        password: userData.password,
        designation: userData.designation || 'Project Monitoring Officer',
        ministry: userData.ministry || 'Ministry of Statistics and Programme Implementation',
        role: userData.role || 'Review Authority'
      });
      if (data && data.token) {
        setUser(data);
        setToken(data.token);
        return { success: true, user: data };
      }
      return { success: false, error: 'Failed to register officer credentials.' };
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Registration failed.';
      return { success: false, error: msg };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    try {
      localStorage.removeItem('paimana_auth_user');
      localStorage.removeItem('paimana_auth_token');
      sessionStorage.clear();
    } catch (e) {
      console.error('Error clearing auth storage:', e);
    }
  };

  const isDemoMode = Boolean(
    user && (
      user.isDemoAccount ||
      user.email?.toLowerCase().trim() === 'v.3@gmail.com' ||
      user.email?.toLowerCase().trim() === 'v.3'
    )
  );

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isDemoMode,
        login,
        register,
        logout,
        demoProfiles: DEMO_PROFILES,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
