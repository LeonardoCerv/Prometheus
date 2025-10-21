"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/sidebar";
import Dashboard from "@/components/dashboard";
import { db } from "@/lib/firebase";
import { doc, getDoc } from "firebase/firestore";
import { getCurrentUser, isAuthenticated } from "@/lib/auth";

interface CompanyDetails {
  companyName: string;
  userName: string;
  userRole: string;
  companySize: string;
  industry: string;
  description: string;
}

export default function FindPage() {
  const router = useRouter();
  const [companyDetails, setCompanyDetails] = useState<CompanyDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication first
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }

    const user = getCurrentUser();
    if (!user) {
      router.push("/");
      return;
    }

    // Load company details from Firebase using user ID
    const loadCompanyDetails = async () => {
      try {
        const docRef = doc(db, "companyProfiles", user.userId);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          const data = docSnap.data() as CompanyDetails;
          setCompanyDetails(data);
        } else {
          // Redirect to sign-up if no company details found
          router.push("/find/sign-up");
          return;
        }
      } catch (error) {
        console.error("Error loading company details:", error);
        router.push("/find/sign-up");
      }

      setIsLoading(false);
    };

    loadCompanyDetails();
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
