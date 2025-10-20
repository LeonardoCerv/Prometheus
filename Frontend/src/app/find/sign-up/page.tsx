"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

type UserType = "corporate" | "startup" | "freelancer";

export default function SignUpPage() {
  const router = useRouter();
  const [selectedType, setSelectedType] = useState<UserType | null>(null);

  const handleContinue = () => {
    if (!selectedType) return;

    // Store the user type for later use
    localStorage.setItem("userType", selectedType);

    if (selectedType === "startup") {
      router.push("/find/startup-details");
    } else if (selectedType === "corporate") {
      // TODO: Implement corporate flow
      alert("Corporate flow coming soon! For now, please use the startup flow.");
      setSelectedType(null);
    } else if (selectedType === "freelancer") {
      // TODO: Implement freelancer flow
      alert("Freelancer flow coming soon! For now, please use the startup flow.");
      setSelectedType(null);
    }
  };

  const options = [
    {
      type: "corporate" as UserType,
      title: "Corporate",
      description: "Looking for stable, long-term talent with low turnover",
      icon: (
        <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
    },
    {
      type: "startup" as UserType,
      title: "Startup",
      description: "Seeking versatile talent for fast-paced, innovative environments",
      icon: (
        <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
    },
    {
      type: "freelancer" as UserType,
      title: "Looking for Freelancer",
      description: "Need temporary or project-based talent for specific work",
      icon: (
        <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  ];

  return (
    <main className="flex w-full flex-1 flex-col min-h-screen bg-background">
      <div className="flex-1 flex flex-col px-4 py-8">
        {/* Logo and Back Button */}
        <div className="flex justify-between items-center px-4 mb-12">
          <a href="/" className="flex items-center gap-4">
            <img src="/prometheus.svg" alt="Logo" width="64" height="64" />
            <p className="text-2xl font-medium leading-6 tracking-base text-foreground font-cormorant">
              <span className="text-primary text-2xl font-averia font-semibold">Prometheus</span>
            </p>
          </a>
          <button
            onClick={() => router.back()}
            className="relative inline-flex items-center justify-center text-base font-semibold tracking-base shadow ring-offset-background transition-colors focus-visible:outline-none disabled:opacity-50 border border-muted hover:bg-background/80 h-[42px] px-8 py-2 text-foreground"
          >
            back
          </button>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex items-center justify-center">
          <div className="w-full max-w-4xl">
            {/* Title */}
            <div className="text-center mb-12 -mt-16">
              <h1 className="text-6xl font-extrabold tracking-tighter text-foreground font-inter mb-4">
                find talent.
              </h1>
              <p className="text-lg font-medium leading-6 tracking-base text-primary mb-8">
                Tell us about your hiring needs
              </p>
            </div>

            {/* Selection Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              {options.map((option) => (
                <button
                  key={option.type}
                  onClick={() => setSelectedType(option.type)}
                  className={`p-8 border-2 transition-all duration-200 hover:shadow-lg ${
                    selectedType === option.type
                      ? "border-primary bg-primary/5 shadow-md"
                      : "border-muted hover:border-primary/50"
                  }`}
                >
                  <div className="flex flex-col items-center text-center gap-4">
                    <div className={`p-3 rounded-full ${
                      selectedType === option.type ? "bg-primary text-background" : "bg-muted text-muted"
                    }`}>
                      {option.icon}
                    </div>
                    <h3 className="text-xl font-bold text-foreground">{option.title}</h3>
                    <p className="text-sm text-muted leading-relaxed">{option.description}</p>
                  </div>
                </button>
              ))}
            </div>

            {/* Continue Button */}
            <div className="text-center">
              <button
                onClick={handleContinue}
                disabled={!selectedType}
                className="bg-primary text-foreground px-12 py-4 font-semibold text-lg hover:brightness-95 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
              >
                continue
              </button>
              {selectedType && (
                <p className="text-sm text-muted mt-4">
                  Selected: <span className="font-semibold text-primary capitalize">{selectedType}</span>
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}