"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function SignUpPage() {
  const router = useRouter();

  useEffect(() => {
    // Automatically redirect to company details
    router.push("/find/company-details");
  }, [router]);

  return (
    <main className="flex w-full flex-1 flex-col min-h-screen bg-background">
      <div className="flex-1 flex flex-col px-4 py-8">
        {/* Logo */}
        <div className="flex justify-center items-center px-4 mb-12">
          <a href="/" className="flex items-center gap-4">
            <img src="/prometheus.svg" alt="Logo" width="64" height="64" />
            <p className="text-2xl font-medium leading-6 tracking-base text-foreground font-cormorant">
              <span className="text-primary text-2xl font-averia font-semibold">Prometheus</span>
            </p>
          </a>
        </div>

        {/* Loading */}
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted">Redirecting...</p>
          </div>
        </div>
      </div>
    </main>
  );
}