"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/sidebar";
import Dashboard from "@/components/dashboard";

interface StartupDetails {
  companyName: string;
  userName: string;
  userRole: string;
  companySize: string;
  industry: string;
  fundingStage: string;
  location: string;
  website: string;
  description: string;
}

export default function FindPage() {
  const router = useRouter();
  const [startupDetails, setStartupDetails] = useState<StartupDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load startup details from localStorage
    const storedDetails = localStorage.getItem("startupDetails");
    const userType = localStorage.getItem("userType");

    if (storedDetails && userType === "startup") {
      setStartupDetails(JSON.parse(storedDetails));
    } else {
      // Redirect to sign-up if no startup details found
      router.push("/find/sign-up");
      return;
    }

    setIsLoading(false);
  }, [router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Sidebar />
      <Dashboard />
    </>
  );
}
