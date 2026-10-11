import React, { useState, useEffect } from 'react';

// Multilingual translations
const I18N = {
  en: {
    platformName: "Growth Grid",
    tagline: "AI-Powered Adaptive STEM Mastery",
    dashboard: "Dashboard",
    adaptiveQuiz: "Adaptive Quiz",
    knowledgeGraph: "Knowledge Graph",
    aiTutor: "AI Tutor",
    credentials: "On-Chain Badges",
    educatorPortal: "Educator Portal",
    streak: "Streak",
    xp: "XP",
    masteryGate: "80% Required to Unlock",
    whyThis: "Why this recommendation?",
    startQuiz: "Start Practice",
    mailId: "Mail ID / Email Address",
    password: "Password",
    signIn: "Sign In & Start Learning",
    signOut: "Sign Out",
    welcomeTitle: "Sign in to Growth Grid",
    welcomeSubtitle: "Enter your registered Mail ID and password to access your adaptive learning dashboard."
  },
  ta: {
    platformName: "குரோத் கிரிட்",
    tagline: "செயற்கை நுண்ணறிவு அடிப்படையிலான STEM கல்வி முறை",
    dashboard: "முகப்பு",
    adaptiveQuiz: "தழுவல் வினாடி வினா",
    knowledgeGraph: "அறிவு வரைபடம்",
    aiTutor: "AI ஆசிரியர்",
    credentials: "சான்றிதழ்கள்",
    educatorPortal: "ஆசிரியர் தளம்",
    streak: "தொடர்",
    xp: "மதிப்பெண்",
    masteryGate: "80% தேர்ச்சி தேவை",
    whyThis: "இந்த பரிந்துரை ஏன்?",
    startQuiz: "பயிற்சி தொடங்க",
    mailId: "மின்னஞ்சல் முகவரி",
    password: "கடவுச்சொல்",
    signIn: "உள்நுழைந்து தொடங்கவும்",
    signOut: "வெளியேறு",
    welcomeTitle: "குரோத் கிரிட்டில் உள்நுழையவும்",
    welcomeSubtitle: "உங்கள் தனிப்பயனாக்கப்பட்ட STEM கற்றல் தளத்திற்கு செல்ல மின்னஞ்சல் மற்றும் கடவுச்சொல்லை உள்ளிடவும்."
  },
  hi: {
    platformName: "ग्रोथ ग्रिड",
    tagline: "एआई-संचालित अनुकूली एसटीईएम शिक्षण",
    dashboard: "डैशबोर्ड",
    adaptiveQuiz: "अनुकूली प्रश्नोत्तरी",
    knowledgeGraph: "ज्ञान आरेख",
    aiTutor: "एआई ट्यूटर",
    credentials: "ब्लॉकचेन बैज",
    educatorPortal: "शिक्षक पोर्टल",
    streak: "दैनिक क्रम",
    xp: "एक्सपी",
    masteryGate: "80% आवश्यक",
    whyThis: "यह सिफारिश क्यों?",
    startQuiz: "अभ्यास प्रारंभ",
    mailId: "ईमेल आईडी",
    password: "पासवर्ड",
    signIn: "साइन इन करें और सीखें",
    signOut: "साइन आउट",
    welcomeTitle: "ग्रोथ ग्रिड में साइन इन करें",
    welcomeSubtitle: "अपने अनुकूली शिक्षण डैशबोर्ड तक पहुंचने के लिए अपनी मेल आईडी और पासवर्ड दर्ज करें।"
  }
};

export default function App() {
  // Authentication State
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState("");
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [regName, setRegName] = useState("");
  const [regSubject, setRegSubject] = useState("Algebra");
  const [regConsent, setRegConsent] = useState(true);

  // App Navigation & Role State
  const [role, setRole] = useState("student");
  const [lang, setLang] = useState("en");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [streak, setStreak] = useState(5);
  const [xp, setXp] = useState(420);
  const [mastery, setMastery] = useState(58);
  const [showWhyModal, setShowWhyModal] = useState(false);

  const t = I18N[lang] || I18N.en;

  // Authentication Handlers
  const handleLoginSubmit = (e) => {
    if (e) e.preventDefault();
    setLoginError("");

    if (!loginEmail.trim()) {
      setLoginError("Please enter your Mail ID.");
      return;
    }
    if (!loginPassword.trim()) {
      setLoginError("Please enter your password.");
      return;
    }

    setIsLoggingIn(true);
    setTimeout(() => {
      setIsLoggingIn(false);
      const emailLower = loginEmail.trim().toLowerCase();

      let userRole = "student";
      let userName = "Alex Student";
      let userCluster = "Steady";

      if (emailLower.includes("educator") || emailLower.includes("teacher") || emailLower.includes("vance")) {
        userRole = "educator";
        userName = "Dr. Evelyn Vance";
        userCluster = "Fast";
        setActiveTab("educator");
      } else if (emailLower.includes("admin")) {
        userRole = "admin";
        userName = "System Administrator";
        userCluster = "Fast";
        setActiveTab("admin");
      } else {
        userRole = "student";
        userName = (emailLower === "student@growthgrid.org" || !emailLower.includes("@")) 
          ? "Alex Student" 
          : emailLower.split("@")[0].replace(/[._]/g, " ").replace(/\b\w/g, c => c.toUpperCase());
        userCluster = "Steady";
        setActiveTab("dashboard");
      }

      setRole(userRole);
      setCurrentUser({
        name: userName,
        email: loginEmail,
        role: userRole,
        cluster: userCluster
      });
      setIsAuthenticated(true);
    }, 450);
  };

  const handleQuickFill = (roleType) => {
    setLoginError("");
    setIsLoggingIn(true);
    setTimeout(() => {
      setIsLoggingIn(false);
      if (roleType === "student") {
        setLoginEmail("student@growthgrid.org");
        setLoginPassword("password123");
        setRole("student");
        setActiveTab("dashboard");
        setCurrentUser({
          name: "Alex Student",
          email: "student@growthgrid.org",
          role: "student",
          cluster: "Steady"
        });
      } else if (roleType === "educator") {
        setLoginEmail("educator@growthgrid.org");
        setLoginPassword("password123");
        setRole("educator");
        setActiveTab("educator");
        setCurrentUser({
          name: "Dr. Evelyn Vance",
          email: "educator@growthgrid.org",
          role: "educator",
          cluster: "Fast"
        });
      } else {
        setLoginEmail("admin@growthgrid.org");
        setLoginPassword("password123");
        setRole("admin");
        setActiveTab("admin");
        setCurrentUser({
          name: "System Administrator",
          email: "admin@growthgrid.org",
          role: "admin",
          cluster: "Fast"
        });
      }
      setIsAuthenticated(true);
    }, 350);
  };

  const handleRegisterSubmit = (e) => {
    if (e) e.preventDefault();
    setLoginError("");

    if (!regName.trim() || !loginEmail.trim() || !loginPassword.trim()) {
      setLoginError("Please fill in all registration fields.");
      return;
    }
    if (!regConsent) {
      setLoginError("Please accept privacy and algorithmic tracking consent.");
      return;
    }

    setIsLoggingIn(true);
    setTimeout(() => {
      setIsLoggingIn(false);
      setRole("student");
      setActiveTab("dashboard");
      setCurrentUser({
        name: regName.trim(),
        email: loginEmail.trim(),
        role: "student",
        cluster: "Steady",
        subject: regSubject
      });
      setIsAuthenticated(true);
    }, 500);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setLoginPassword("");
    setLoginError("");
    setIsRegisterMode(false);
  };

  // -------------------------------------------------------------
  // LOGIN SCREEN (FIRST SCREEN BEFORE APP GETS STARTED)
  // -------------------------------------------------------------
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100 flex flex-col justify-between selection:bg-sky-500 selection:text-white font-sans">
        
        {/* Top Minimal Header */}
        <header className="px-6 py-4 flex items-center justify-between border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 via-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20 text-white font-black text-xl">
              G²
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg text-white tracking-tight">{t.platformName}</span>
                <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30">
                  Adaptive Portal
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">{t.tagline}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs text-slate-300 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-sky-500"
            >
              <option value="en">English</option>
              <option value="ta">தமிழ் (Tamil)</option>
              <option value="hi">हिन्दी (Hindi)</option>
            </select>
          </div>
        </header>

        {/* Central Card */}
        <div className="flex-1 flex items-center justify-center p-4 sm:p-6 my-6">
          <div className="max-w-md w-full bg-slate-900/90 backdrop-blur-xl border border-slate-800 rounded-3xl shadow-2xl p-6 sm:p-8 relative overflow-hidden space-y-6">
            
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-sky-600 via-sky-400 to-indigo-600"></div>

            <div className="text-center space-y-2">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-600 via-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/30 text-white font-extrabold text-2xl mx-auto">
                G²
              </div>
              <h2 className="text-2xl font-extrabold text-white tracking-tight">
                {isRegisterMode ? "Create Your Account" : t.welcomeTitle}
              </h2>
              <p className="text-xs text-slate-400 max-w-xs mx-auto">
                {isRegisterMode 
                  ? "Start your personalized adaptive STEM learning path with Bayesian Knowledge Tracing."
                  : t.welcomeSubtitle}
              </p>
            </div>

            {/* Mode Tabs */}
            <div className="flex items-center p-1 bg-slate-950/80 rounded-2xl border border-slate-800">
              <button
                type="button"
                onClick={() => { setIsRegisterMode(false); setLoginError(""); }}
                className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${!isRegisterMode ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30' : 'text-slate-400 hover:text-white'}`}
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => { setIsRegisterMode(true); setLoginError(""); }}
                className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${isRegisterMode ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30' : 'text-slate-400 hover:text-white'}`}
              >
                New Student
              </button>
            </div>

            {/* Error Message */}
            {loginError && (
              <div className="p-3 bg-rose-950/40 border border-rose-500/50 rounded-xl text-xs text-rose-300 flex items-center gap-2">
                <span>⚠️</span>
                <span>{loginError}</span>
              </div>
            )}

            {/* Sign In Mode */}
            {!isRegisterMode ? (
              <form onSubmit={handleLoginSubmit} className="space-y-4">
                <div className="space-y-1.5 text-left">
                  <label className="text-xs font-semibold text-slate-300 flex items-center justify-between">
                    <span>{t.mailId}</span>
                    <span className="text-[10px] text-sky-400 font-normal">student@growthgrid.org</span>
                  </label>
                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-sm">✉️</span>
                    <input
                      type="email"
                      required
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                      placeholder="e.g. student@growthgrid.org"
                      className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 pl-10 pr-4 text-xs text-white placeholder-slate-500 focus:outline-none transition-colors"
                    />
                  </div>
                </div>

                <div className="space-y-1.5 text-left">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-semibold text-slate-300">{t.password}</label>
                    <span className="text-[10px] text-slate-400 font-normal">Demo: password123</span>
                  </div>
                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-sm">🔒</span>
                    <input
                      type={showPassword ? "text" : "password"}
                      required
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 pl-10 pr-10 text-xs text-white placeholder-slate-500 focus:outline-none transition-colors"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xs"
                    >
                      {showPassword ? "🙈" : "👁️"}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="rounded bg-slate-950 border-slate-700 text-sky-500 focus:ring-0"
                    />
                    <span>Remember me</span>
                  </label>
                  <span className="text-[11px] text-sky-400">Secure JWT RBAC</span>
                </div>

                <button
                  type="submit"
                  disabled={isLoggingIn}
                  className="w-full py-3.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition-all flex items-center justify-center gap-2 cursor-pointer"
                >
                  {isLoggingIn ? "Authenticating..." : `${t.signIn} →`}
                </button>
              </form>
            ) : (
              /* Register Mode */
              <form onSubmit={handleRegisterSubmit} className="space-y-4">
                <div className="space-y-1.5 text-left">
                  <label className="text-xs font-semibold text-slate-300">Full Name</label>
                  <input
                    type="text"
                    required
                    value={regName}
                    onChange={(e) => setRegName(e.target.value)}
                    placeholder="e.g. Sai Krupa"
                    className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 px-3.5 text-xs text-white placeholder-slate-500 focus:outline-none"
                  />
                </div>

                <div className="space-y-1.5 text-left">
                  <label className="text-xs font-semibold text-slate-300">{t.mailId}</label>
                  <input
                    type="email"
                    required
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    placeholder="e.g. newstudent@growthgrid.org"
                    className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 px-3.5 text-xs text-white placeholder-slate-500 focus:outline-none"
                  />
                </div>

                <div className="space-y-1.5 text-left">
                  <label className="text-xs font-semibold text-slate-300">{t.password}</label>
                  <input
                    type="password"
                    required
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="Create a strong password"
                    className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 px-3.5 text-xs text-white placeholder-slate-500 focus:outline-none"
                  />
                </div>

                <div className="space-y-1.5 text-left">
                  <label className="text-xs font-semibold text-slate-300">Starting STEM Subject</label>
                  <select
                    value={regSubject}
                    onChange={(e) => setRegSubject(e.target.value)}
                    className="w-full bg-slate-950/80 border border-slate-700/80 focus:border-sky-500 rounded-xl py-3 px-3.5 text-xs text-white focus:outline-none"
                  >
                    <option value="Algebra">📐 Algebra & Functions</option>
                    <option value="Physics">⚡ Physics Fundamentals</option>
                    <option value="Coding">💻 Coding Fundamentals</option>
                  </select>
                </div>

                <label className="flex items-start gap-2 text-[11px] text-slate-400 cursor-pointer pt-1 text-left">
                  <input
                    type="checkbox"
                    checked={regConsent}
                    onChange={(e) => setRegConsent(e.target.checked)}
                    className="rounded bg-slate-950 border-slate-700 text-sky-500 focus:ring-0 mt-0.5"
                  />
                  <span>I agree to adaptive Bayesian skill modeling and anonymous Polygon on-chain credentialing (Zero PII).</span>
                </label>

                <button
                  type="submit"
                  disabled={isLoggingIn}
                  className="w-full py-3.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/30 transition-all flex items-center justify-center gap-2 cursor-pointer"
                >
                  {isLoggingIn ? "Creating Profile..." : "Create Account & Start Learning →"}
                </button>
              </form>
            )}

            {/* Quick 1-Click Fast Logins */}
            <div className="pt-2 border-t border-slate-800 space-y-2.5">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider text-center">
                ⚡ Instant 1-Click Demo Accounts
              </div>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleQuickFill("student")}
                  className="p-2.5 rounded-xl bg-slate-950/90 hover:bg-slate-800 border border-slate-800 hover:border-sky-500 text-slate-200 text-[11px] font-semibold flex flex-col items-center gap-1 transition-all cursor-pointer"
                >
                  <span className="text-base">🎓</span>
                  <span className="text-white">Student</span>
                  <span className="text-[9px] text-slate-500 font-normal">Alex (Steady)</span>
                </button>

                <button
                  type="button"
                  onClick={() => handleQuickFill("educator")}
                  className="p-2.5 rounded-xl bg-slate-950/90 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500 text-slate-200 text-[11px] font-semibold flex flex-col items-center gap-1 transition-all cursor-pointer"
                >
                  <span className="text-base">👩‍🏫</span>
                  <span className="text-white">Educator</span>
                  <span className="text-[9px] text-slate-500 font-normal">Dr. Vance</span>
                </button>

                <button
                  type="button"
                  onClick={() => handleQuickFill("admin")}
                  className="p-2.5 rounded-xl bg-slate-950/90 hover:bg-slate-800 border border-slate-800 hover:border-amber-500 text-slate-200 text-[11px] font-semibold flex flex-col items-center gap-1 transition-all cursor-pointer"
                >
                  <span className="text-base">⚙️</span>
                  <span className="text-white">Admin</span>
                  <span className="text-[9px] text-slate-500 font-normal">LMS / System</span>
                </button>
              </div>
            </div>

          </div>
        </div>

        {/* Footer */}
        <footer className="py-4 border-t border-slate-800/80 text-center text-xs text-slate-500">
          Growth Grid © 2026 • AI-Powered STEM Adaptive Learning Platform • Bayesian Knowledge Tracing • Polygon Testnet
        </footer>

      </div>
    );
  }

  // -------------------------------------------------------------
  // AUTHENTICATED PLATFORM APP
  // -------------------------------------------------------------
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      
      {/* Header with User Info and Logout */}
      <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 via-sky-500 to-indigo-600 flex items-center justify-center font-black text-xl text-white shadow-lg shadow-sky-500/20">
            G²
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-white">{t.platformName}</span>
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30">
                BKT + RAG + Polygon
              </span>
            </div>
            <p className="text-xs text-slate-400">{t.tagline}</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-2">
          {['dashboard', 'quiz', 'graph', 'tutor', 'credentials'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all ${activeTab === tab ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
            >
              {tab}
            </button>
          ))}
        </nav>

        {/* Controls: User profile, Role, Language, Sign Out */}
        <div className="flex items-center gap-2">
          {/* User Badge */}
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1.5 rounded-xl bg-slate-800/90 border border-slate-700 text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-semibold text-white">
              {currentUser?.name || "Alex Student"}
            </span>
            <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300">
              {role}
            </span>
          </div>

          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-sky-300 rounded-lg px-2.5 py-1.5 focus:outline-none"
          >
            <option value="student">Student (Alex)</option>
            <option value="educator">Educator (Dr. Vance)</option>
            <option value="admin">Admin (LMS)</option>
          </select>

          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-300 rounded-lg px-2 py-1.5 focus:outline-none"
          >
            <option value="en">EN</option>
            <option value="ta">தமிழ்</option>
            <option value="hi">हिन्दी</option>
          </select>

          {/* Sign Out Button */}
          <button
            onClick={handleLogout}
            title={t.signOut}
            className="px-2.5 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <span>🚪</span>
            <span className="hidden sm:inline">{t.signOut}</span>
          </button>
        </div>
      </header>

      {/* Main Body */}
      <main className="flex-1 max-w-7xl mx-auto w-full p-6 space-y-6">
        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 flex items-center gap-4">
            <span className="text-3xl">🔥</span>
            <div>
              <p className="text-xs text-slate-400 uppercase font-semibold">{t.streak}</p>
              <h3 className="text-2xl font-bold text-white">{streak} Days</h3>
            </div>
          </div>
          <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 flex items-center gap-4">
            <span className="text-3xl">⭐</span>
            <div>
              <p className="text-xs text-slate-400 uppercase font-semibold">{t.xp}</p>
              <h3 className="text-2xl font-bold text-amber-300">{xp}</h3>
            </div>
          </div>
          <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 flex items-center gap-4">
            <span className="text-3xl">🧠</span>
            <div>
              <p className="text-xs text-slate-400 uppercase font-semibold">Learner Cluster</p>
              <h3 className="text-lg font-bold text-sky-300">Steady Learner</h3>
            </div>
          </div>
          <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 flex items-center gap-4">
            <span className="text-3xl">⛓️</span>
            <div>
              <p className="text-xs text-slate-400 uppercase font-semibold">Polygon Badges</p>
              <h3 className="text-2xl font-bold text-purple-300">1 Verified</h3>
            </div>
          </div>
        </div>

        {/* Hero Recommendation Card */}
        <div className="bg-gradient-to-r from-slate-800 to-sky-950/40 border border-sky-500/30 rounded-3xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-xs font-semibold text-sky-300">
              ⚡ Real-Time BKT Recommendation
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              Linear Equations & Inequalities
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Prerequisite mastery in <strong>Fractions (88%)</strong> is solid! Your current mastery is <strong>{mastery}%</strong>. Clear the 80% gate to unlock Systems of Equations.
            </p>
            <div className="flex items-center gap-3 pt-2">
              <button
                onClick={() => setActiveTab("quiz")}
                className="px-6 py-3 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-sm shadow-lg shadow-sky-600/30 transition-all cursor-pointer"
              >
                {t.startQuiz} →
              </button>
              <button
                onClick={() => setShowWhyModal(true)}
                className="px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 font-medium text-sm transition-all cursor-pointer"
              >
                💡 {t.whyThis}
              </button>
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-700 rounded-2xl p-6 text-center min-w-[200px]">
            <div className="text-4xl font-extrabold text-sky-400">{mastery}%</div>
            <p className="text-xs text-slate-400 uppercase font-semibold mt-1">BKT P(L)</p>
            <div className="text-[10px] text-amber-400 mt-2 font-medium">{t.masteryGate}</div>
          </div>
        </div>

        {/* Standalone Preview Notice */}
        <div className="p-4 rounded-2xl bg-slate-800/40 border border-slate-700 text-xs text-slate-400 flex items-center justify-between">
          <span>💡 Note: You can open <code>preview.html</code> directly in any browser for the full interactive simulation.</span>
          <span className="text-sky-400">FastAPI API Docs: <code>/docs</code></span>
        </div>
      </main>

      {/* XAI Explanation Modal */}
      {showWhyModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-sky-500/50 rounded-3xl p-6 max-w-md w-full space-y-4">
            <h3 className="font-extrabold text-white text-lg">💡 Why this recommendation?</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              1. <strong>BKT Score:</strong> Current mastery is 58% (below the 80% Mastery Gate).<br />
              2. <strong>Prerequisite Check:</strong> Foundational skill "Fractions" is 88% (Satisfied).<br />
              3. <strong>Cluster:</strong> Steady learner profile assigns Level 2–3 scaffolding.
            </p>
            <button
              onClick={() => setShowWhyModal(false)}
              className="w-full py-2.5 rounded-xl bg-sky-600 text-white font-bold text-xs cursor-pointer"
            >
              Understood
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
